import os
import pandas as pd
import requests
from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory
from flask_paginate import Pagination
from pandas import DataFrame
import config
from extensao import db
from models.arquivo import Arquivo
from models.campos import Campo
from models.dado import Dado
from models.fonte import Fonte

web = Blueprint('web', __name__)


@web.route('/')
def index():
    return render_template('index.html')


@web.route('/buscar/', methods=['POST', ])
def buscar():
    site = request.form['site']
    separador = request.form['separador']

    try:
        arquivo = download_file(site)
        tratar_arquivo(arquivo, separador)
    except Exception:
        return print(Exception)

    dataFrame = pd.read_csv(arquivo, sep=separador)
    dataFrame = dataFrame.dropna(how='all')
    dataFrame = dataFrame.dropna(axis=1, how='all')
    dataFrame = dataFrame.dropna()

    criar_fonte(site, site)

    fonte = Fonte.query.filter_by(site=site).first()

    criar_arquivo(arquivo, separador, fonte)

    arquivo = Arquivo.query.filter_by(fonte=fonte.id).first()

    criar_campo(dataFrame, arquivo)

    if os.path.exists(arquivo.titulo):
        os.remove(arquivo.titulo)

    return redirect(url_for('web.listar'))


@web.route('/listar/')
def listar():
    arquivo = Arquivo.query.all()
    return render_template('table/list_tables.html', arquivos=arquivo)


@web.route('/visualizar/<id>')
def visualizar(id):
    arquivo = Arquivo.query.filter_by(id=id).first()
    campos = Campo.query.filter_by(arquivo=arquivo.id)
    local = os.path.join(config.UPLOAD_FOLDER, arquivo.titulo)
    if os.path.exists(local):
        os.remove(local)

    table = dict()
    quantidade = 0
    PER_PAGE = 20
    search = False
    q = request.args.get('q')
    if q:
        search = True
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1

    for campo in campos:
        dado = []
        dados = Dado.query.filter_by(campo=campo.id)
        title = str(campo.nome).title()
        for data in dados:
            dado.append(data.valor)
        table[title] = dado
        quantidade = len(table[title])
    pagination = Pagination(page=page, total=quantidade, search=search, record_name='records', per_page=PER_PAGE)
    data = pd.DataFrame(table)
    data_col = list(data.keys())

    return render_template('table/render_table.html',
                           tabela=data[(page - 1) * PER_PAGE:page * PER_PAGE][data_col].to_html(),
                           arquivo=arquivo, pagination=pagination)


@web.route('/baixar/<id>')
def baixar(id):
    table = dict()
    arquivo = Arquivo.query.filter_by(id=id).first()
    campos = Campo.query.filter_by(arquivo=arquivo.id)
    for campo in campos:
        dado = []
        dados = Dado.query.filter_by(campo=campo.id)
        for data in dados:
            dado.append(data.valor)
        table[campo.nome] = dado
    local = os.path.join(config.UPLOAD_FOLDER, arquivo.titulo)
    if not os.path.exists(local):
        pd.DataFrame(table).to_csv(path_or_buf=local, encoding='utf-8', sep=',', index=False)
    return send_from_directory(directory=config.UPLOAD_FOLDER, path=arquivo.titulo, mimetype='text/csv', as_attachment=True)


def download_file(url):
    local_filename = rename_file(url.split('/')[-1])
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def rename_file(file):
    local_filename = file.split('.')[-1]
    if not local_filename == 'csv':
        return str(file.split('.')[-2]) + '.csv'
    return file


def tratar_arquivo(arquivo, separador):
    try:
        with open(arquivo, 'r', encoding='latin-1') as fr:
            # reading line by line
            lines = fr.readlines()

            # opening in writing mode
            with open(arquivo, 'w', encoding="utf-8") as fw:
                for line in lines:

                    if line.find(separador) != -1:
                        fw.write(line)
        fr.close()
        fw.close()

        print("Tratado")

    except:
        print("Oops! algum erro.")


def criar_fonte(url: str, site: str):
    fonte = Fonte(url=url, site=site)
    db.session.add(fonte)
    db.session.commit()


def criar_arquivo(titulo: str, separador: str, fonte: Fonte):
    file = Arquivo(titulo=titulo, separador=separador, fonte=fonte.id)
    db.session.add(file)
    db.session.commit()


def criar_campo(data: DataFrame, arquivo: Arquivo):
    for nome in data.columns:
        campo = Campo(nome=nome, arquivo=arquivo.id)

        db.session.add(campo)
        db.session.commit()

        campo = Campo.query.filter_by(arquivo=arquivo.id).filter_by(nome=nome).first()
        criar_dados(data, campo)


def criar_dados(dataFrame: DataFrame, campo: Campo):
    lista = []
    count = 0
    total = len(dataFrame[campo.nome]) - 1

    for data in dataFrame[campo.nome]:
        dado = Dado(valor=data, index=count, campo=campo.id)
        lista.append(dado)
        if count % 100 == 0 or count == total:
            db.session.add_all(lista)
            db.session.commit()
            lista = []
        count += 1
