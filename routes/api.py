import os
import pandas as pd
from dicttoxml import dicttoxml
from flask import Blueprint, request, render_template
from flask_paginate import Pagination
from models.arquivo import Arquivo
from models.campos import Campo
from models.dado import Dado
from models.fonte import Fonte
from routes import inicio

api = Blueprint('api', __name__)


@api.route('/api/buscar/', methods=['POST', ])
def buscar_api():
    site = request.form['site']
    separador = request.form['separador']

    arquivo = inicio.download_file(site)
    inicio.tratar_arquivo(arquivo, separador)

    dataFrame = pd.read_csv(arquivo, sep=separador)
    dataFrame = dataFrame.dropna(how='all')
    dataFrame = dataFrame.dropna(axis=1, how='all')

    inicio.criar_fonte(site, site)

    fonte = Fonte.query.filter_by(site=site).first()

    inicio.criar_arquivo(arquivo, separador, fonte)

    arquivo = Arquivo.query.filter_by(fonte=fonte.id).first()

    inicio.criar_campo(dataFrame, arquivo)

    if os.path.exists(arquivo.titulo):
        os.remove(arquivo.titulo)

    return {
        'ok': 'Busca realziada com sucesso'
    }


@api.route('/api/listar/', methods=['POST',])
def listar_api():
    arquivos = Arquivo.query.all()
    lista = dict()
    for arquivo in arquivos:
        arquivo.__dict__.pop('_sa_instance_state', None)
        a = arquivo.__dict__
        lista[arquivo.id] = a
    xml = dicttoxml(lista, attr_type=False, custom_root='Arquivo')
    return xml


@api.route('/api/listar/<id>', methods=['POST',])
def listar_api_id(id):
    arquivo = Arquivo.query.filter_by(id=id).first()
    campos = Campo.query.filter_by(arquivo=arquivo.id)
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
    pagination = Pagination(page=page, total=quantidade, search=search, record_name='records', per_page=PER_PAGE)
    data = pd.DataFrame(table)
    data_col = list(data.keys())
    return render_template('xml/template.xml', tabela=data[(page - 1) * PER_PAGE:page * PER_PAGE][data_col].to_xml(), pagination=pagination)
