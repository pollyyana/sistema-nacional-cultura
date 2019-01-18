import os, sys
import environ
import csv
import django
import pandas as pd

from datetime import datetime as dt

# from django.conf import settings
# from snc import settings as snc_settings

# ROOT_DIR = environ.Path(__file__)
# sys.path.append(ROOT_DIR)
# settings.configure(default_settings=snc_settings, DEBUG=True)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'snc.settings')
django.setup()

from adesao.models import SistemaCultura, EnteFederado

UFS = {
    "RONDÔNIA": 11,
    "ACRE": 12,
    "AMAZONAS": 13,
    "RORAIMA": 14,
    "PARÁ": 15,
    "AMAPÁ": 16,
    "TOCANTINS": 17,
    "MARANHÃO": 21,
    "PIAUÍ": 22,
    "CEARÁ": 23,
    "RIO GRANDE DO NORTE": 24,
    "PARAÍBA": 25,
    "PERNAMBUCO": 26,
    "ALAGOAS": 27,
    "SERGIPE": 28,
    "BAHIA": 29,
    "MINAS GERAIS": 31,
    "ESPÍRITO SANTO": 32,
    "RIO DE JANEIRO": 33,
    "SÃO PAULO": 35,
    "PARANÁ": 41,
    "SANTA CATARINA": 42,
    "RIO GRANDE DO SUL": 43,
    "MATO GROSSO DO SUL": 50,
    "MATO GROSSO": 51,
    "GOIÁS": 52,
    "DISTRITO FEDERAL": 53
}

with open("adesao/fixtures/planilha.csv") as file:
    i = csv.DictReader(file)

    for df in i:
        sistemas = None
        sistema = None

        ente = df['ente'].strip()
        estado_do_processo = df['estado_do_processo']
        data_adesao = df['data_adesao']

        if estado_do_processo == estado_do_processo:
            estado_do_processo = estado_do_processo.strip()

        if data_adesao == data_adesao:
            data_adesao = data_adesao.strip()

        if ente.isupper():
            codigo_ibge = UFS[ente]
            nome_estado = ente

        sistemas = SistemaCultura.sistema.filter(ente_federado__nome__unaccent__iexact=ente, ente_federado__cod_ibge__startswith=codigo_ibge)

        if len(sistemas) > 1:
            if ente.isupper():
                sistema = sistemas.filter(ente_federado__cod_ibge=codigo_ibge)[0]
            else:
                sistema = sistemas.exclude(ente_federado__cod_ibge=codigo_ibge)[0]
        elif len(sistemas) == 0:
            try:
                entefederado = EnteFederado.objects.get(nome__unaccent__iexact=ente, cod_ibge__startswith=codigo_ibge)
            except EnteFederado.DoesNotExist:
                print(f"{ente} - {UFS[nome_estado]} - Planilha: {estado_do_processo}")
                continue

            sistema = SistemaCultura()
            sistema.ente_federado = entefederado
        else:
            sistema = sistemas[0]

        if estado_do_processo in ('1', 'Sim'):
            sistema.estado_processo = '6'
            data_adesao = dt.strptime(data_adesao, '%d/%m/%Y')
            sistema.data_publicacao_acordo = data_adesao
        else:
            if sistema.estado_processo == '6':
                sistema.estado_processo = '0'
                sistema.data_publicacao_acordo = None

        sistema.save()
