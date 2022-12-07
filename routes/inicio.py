import pandas as pd
import requests
from flask import Blueprint, render_template, request

web = Blueprint('web', __name__)


@web.route('/')
def index():
    return render_template('index.html', titulo='login')


@web.route('/buscar/', methods=['POST', 'GET'])
def buscar():
    site = request.form['site']
    separador = request.form['separador']

    try:
        arquivo = download_file(site)
        tratar_arquivo(arquivo, separador)
    except Exception:
        print('Deu capim')
        return print(Exception)

    dataFrame = pd.read_csv(arquivo, sep=separador)
    print(dataFrame)


def download_file(url):
    local_filename = url.split('/')[-2]
    local_filename = rename_file(local_filename)
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb', encoding='cp1252') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename


def rename_file(file):
    local_filename = file.split('.')[-1]
    if not local_filename == 'csv':
        return str(file.split('.')[-2]) + '.csv'


def tratar_arquivo(arquivo, separador):
    try:
        with open(arquivo, 'r', encoding='cp1252') as fr:
            # reading line by line
            lines = fr.readlines()

            # opening in writing mode
            with open(arquivo, 'w', encoding="utf-8") as fw:
                for line in lines:

                    if line.find(separador) != -1:
                        fw.write(line)
        print("Deleted")

    except:
        print("Oops! someting error")
