import pytest
import random
import datetime

from django.urls import reverse

from rest_framework import status
from model_mommy import mommy
from model_mommy.recipe import seq

from planotrabalho.models import SituacoesArquivoPlano
from planotrabalho.models import PlanoTrabalho
from adesao.models import Municipio
from adesao.models import LISTA_ESTADOS_PROCESSO
from planotrabalho.forms import SETORIAIS
from planotrabalho.models import SITUACAO_CONSELHEIRO

pytestmark = pytest.mark.django_db

url_sistemadeculturalocal = reverse("api:sistemacultura-list")
url_acoesplanotrabalho = reverse("api:planotrabalho-list")


def test_municipios_list_endpoint_returning_200_OK(client):

    request = client.get(url_sistemadeculturalocal)

    assert request.status_code == status.HTTP_200_OK


def test_URL_sistema_cultura_local_retorna_10_sistemas(client):

    mommy.make('Municipio', _quantity=12)

    request = client.get(url_sistemadeculturalocal,
                         content_type="application/hal+json")

    assert isinstance(request.data["_embedded"]["items"], list)
    assert len(request.data["_embedded"]["items"]) == 10


def test_404_recupera_ID_sistema_cultura_local(client):

    url = url_sistemadeculturalocal + '45/'

    request = client.get(url, content_type="application/hal+json")

    assert request.status_code == status.HTTP_404_NOT_FOUND


def test_recupera_ID_param_sistema_cultura_local(client, plano_trabalho):

    sistema_de_cultura = Municipio.objects.first()
    municipio_id = '{}/'.format(sistema_de_cultura.id)
    url = url_sistemadeculturalocal + municipio_id

    request = client.get(url, content_type="application/hal+json")

    assert request.status_code == status.HTTP_200_OK
    assert request.data["id"] == sistema_de_cultura.id


def test_entidades_principais_sistema_cultura_local(client, plano_trabalho):

    sistema_de_cultura = Municipio.objects.first()
    municipio_id = '{}/'.format(sistema_de_cultura.id)
    url = url_sistemadeculturalocal + municipio_id

    request = client.get(url, content_type="application/hal+json")

    entidades = set(["governo", "ente_federado", "conselho",
                     "_embedded", "situacao_adesao", "data_adesao",
                     "_links", "id"])

    assert entidades.symmetric_difference(request.data) == set()


def test_campos_do_objeto_governo_ao_retornar_sistema_cultura_local(client,
                                                                    plano_trabalho):

    sistema_de_cultura = Municipio.objects.first()
    municipio_id = '{}/'.format(sistema_de_cultura.id)
    url = url_sistemadeculturalocal + municipio_id

    request = client.get(url, content_type="application/hal+json")

    campos = set(["nome_prefeito", "email_institucional_prefeito",
                  "termo_posse_prefeito"])

    assert campos.symmetric_difference(request.data["governo"]) == set()


def test_campos_do_objeto_ente_federado_ao_retornar_sistema_cultura_local(client,
                                                                          plano_trabalho):
    sistema_de_cultura = Municipio.objects.first()
    municipio_id = '{}/'.format(sistema_de_cultura.id)
    url = url_sistemadeculturalocal + municipio_id

    request = client.get(url, content_type="application/hal+json")

    campos = set(["cnpj_prefeitura", "endereco_eletronico", "telefones", "localizacao"])

    assert campos.symmetric_difference(request.data["ente_federado"]) == set()


def test_campos_do_objeto_estado_ao_retornar_sistema_cultura_local(client,
                                                                          plano_trabalho):
    sistema_de_cultura = Municipio.objects.first()
    municipio_id = '{}/'.format(sistema_de_cultura.id)
    url = url_sistemadeculturalocal + municipio_id

    request = client.get(url, content_type="application/hal+json")

    campos = set(["codigo_ibge", "sigla", "nome_uf"])

    assert campos.symmetric_difference(request.data["ente_federado"]["localizacao"]["estado"]) == set()


def test_campos_do_objeto_embedded_ao_retornar_sistema_cultura_local(client,
                                                                     plano_trabalho):

    sistema_de_cultura = Municipio.objects.first()
    municipio_id = '{}/'.format(sistema_de_cultura.id)
    url = url_sistemadeculturalocal + municipio_id

    request = client.get(url, content_type="application/hal+json")

    campos = set(["acoes_plano_trabalho"])

    assert campos.symmetric_difference(request.data["_embedded"]) == set()


def test_campos_do_objeto_conselho_ao_retornar_sistema_cultura_local(client,
                                                                     plano_trabalho):

    sistema_de_cultura = Municipio.objects.first()
    municipio_id = '{}/'.format(sistema_de_cultura.id)
    url = url_sistemadeculturalocal + municipio_id

    request = client.get(url, content_type="application/hal+json")

    campos = set(["conselheiros"])

    assert campos.symmetric_difference(request.data["conselho"]) == set()


def test_planotrabalho_list_endpoint_returning_200_OK(client):

    request = client.get(url_acoesplanotrabalho)

    assert request.status_code == status.HTTP_200_OK


def test_planotrabalho_list_retorna_lista_com_10(client):

    mommy.make('PlanoTrabalho', 13)

    request = client.get(url_acoesplanotrabalho,
                         content_type="application/hal+json")

    assert isinstance(request.data["_embedded"]["items"], list)
    assert len(request.data["_embedded"]["items"]) == 10


def test_acoesplanotrabalho_retorna_404_para_id_nao_valido(client):

    url = url_acoesplanotrabalho + '55/'

    request = client.get(url, content_type="application/hal+json")

    assert request.status_code == status.HTTP_404_NOT_FOUND


def test_acoesplanotrabalho_retorna_para_id_valido(client, plano_trabalho):

    plano_trabalho = PlanoTrabalho.objects.first()
    plano_trabalho_id = '{}/'.format(plano_trabalho.id)
    url = url_acoesplanotrabalho + plano_trabalho_id

    request = client.get(url, content_type="application/hal+json")

    assert request.status_code == status.HTTP_200_OK
    assert request.data["id"] == plano_trabalho.id


def test_campos_acoesplanotrabalho(client, plano_trabalho):

    plano_trabalho = PlanoTrabalho.objects.first()
    plano_trabalho_id = '{}/'.format(plano_trabalho.id)
    url = url_acoesplanotrabalho + plano_trabalho_id

    request = client.get(url, content_type="application/hal+json")

    campos = set(["criacao_lei_sistema_cultura", "criacao_orgao_gestor",
                  "criacao_plano_cultura", "criacao_fundo_cultura",
                  "criacao_conselho_cultural", "_links", "id", "_embedded"])

    assert campos.symmetric_difference(request.data) == set()


def test_objeto_embedded_acoesplanotrabalho(client, plano_trabalho):

    plano_trabalho = PlanoTrabalho.objects.first()
    plano_trabalho_id = '{}/'.format(plano_trabalho.id)
    url = url_acoesplanotrabalho + plano_trabalho_id

    request = client.get(url, content_type="application/hal+json")

    campos = set(["sistema_cultura_local"])

    assert campos.symmetric_difference(request.data["_embedded"]) == set()


def test_objeto_criacao_lei_sistema_cultura_acoesplanotrabalho(client, plano_trabalho):

    plano_trabalho = PlanoTrabalho.objects.first()
    plano_trabalho_id = '{}/'.format(plano_trabalho.id)
    url = url_acoesplanotrabalho + plano_trabalho_id

    request = client.get(url, content_type="application/hal+json")

    campos = set(["lei_sistema_cultura", "situacao"])

    assert campos.symmetric_difference(request.data["criacao_lei_sistema_cultura"]) == set()


def test_objeto_criacao_orgao_gestor_acoesplanotrabalho(client, plano_trabalho):

    plano_trabalho = PlanoTrabalho.objects.first()
    plano_trabalho_id = '{}/'.format(plano_trabalho.id)
    url = url_acoesplanotrabalho + plano_trabalho_id

    request = client.get(url, content_type="application/hal+json")

    campos = set(["relatorio_atividade_secretaria", "situacao"])

    assert campos.symmetric_difference(request.data["criacao_orgao_gestor"]) == set()


def test_objeto_criacao_plano_cultura_acoesplanotrabalho(client, plano_trabalho):

    plano_trabalho = PlanoTrabalho.objects.first()
    plano_trabalho_id = '{}/'.format(plano_trabalho.id)
    url = url_acoesplanotrabalho + plano_trabalho_id

    request = client.get(url, content_type="application/hal+json")

    campos = set(["relatorio_diretrizes_aprovadas", "minuta_preparada",
                  "ata_reuniao_aprovacao_plano", "ata_votacao_projeto_lei",
                  "lei_plano_cultura", "situacao"])

    assert campos.symmetric_difference(request.data["criacao_plano_cultura"]) == set()


def test_objeto_criacao_fundo_cultura_acoesplanotrabalho(client, plano_trabalho):

    plano_trabalho = PlanoTrabalho.objects.first()
    plano_trabalho_id = '{}/'.format(plano_trabalho.id)
    url = url_acoesplanotrabalho + plano_trabalho_id

    request = client.get(url, content_type="application/hal+json")

    campos = set(["cnpj_fundo_cultura", "lei_fundo_cultura", "situacao"])

    assert campos.symmetric_difference(request.data["criacao_fundo_cultura"]) == set()


def test_objeto_criacao_conselho_cultural_acoesplanotrabalho(client, plano_trabalho):

    plano_trabalho = PlanoTrabalho.objects.first()
    situacao = SituacoesArquivoPlano.objects.first()
    conselho_cultural = mommy.make('ConselhoCultural', situacao=situacao)
    plano_trabalho = mommy.make('PlanoTrabalho', conselho_cultural=conselho_cultural)
    plano_trabalho_id = '{}/'.format(plano_trabalho.id)
    url = url_acoesplanotrabalho + plano_trabalho_id

    request = client.get(url, content_type="application/hal+json")

    campos = set(["ata_regimento_aprovado", "situacao"])

    assert campos.symmetric_difference(request.data["criacao_conselho_cultural"]) == set()


def test_objeto_conselheiros_sistema_de_cultura(client, plano_trabalho):

    sistema_de_cultura = plano_trabalho.usuario.municipio
    sistema_id = '{}/'.format(sistema_de_cultura.id)
    url = url_sistemadeculturalocal + sistema_id

    request = client.get(url, content_type="application/hal+json")

    campos = set(["segmento", "situacao", "data_cadastro", "email",
                  "data_situacao", "nome"])

    assert campos.symmetric_difference(request.data["conselho"]["conselheiros"][0]) == set()


def test_retorno_situacao_conselheiro(client, plano_trabalho):

    sistema_de_cultura = Municipio.objects.first()
    sistema_id = '{}/'.format(sistema_de_cultura.id)
    url = url_sistemadeculturalocal + sistema_id

    request = client.get(url, content_type="application/hal+json")

    situacao = request.data["conselho"]["conselheiros"][0]["situacao"]

    assert situacao == "Habilitado"


def test_retorno_data_adesao_sistema_de_cultura(client, plano_trabalho):

    sistema_de_cultura = Municipio.objects.first()
    sistema_id = '{}/'.format(sistema_de_cultura.id)
    url = url_sistemadeculturalocal + sistema_id

    request = client.get(url, content_type="application/hal+json")

    assert request.data["data_adesao"]
    assert request.data["data_adesao"] == str(sistema_de_cultura.usuario.data_publicacao_acordo)


""" Testes de requisições com parâmetros """


def test_retorno_maximo_de_100_objetos_sistema_de_cultura(client):

    mommy.make('Municipio', cidade__codigo_ibge=seq(110), _quantity=110)
    limit_param = '?limit=150'

    url = url_sistemadeculturalocal + limit_param

    request = client.get(url, content_type="application/hal+json")

    assert len(request.data["_embedded"]["items"]) == 100


def test_retorno_maximo_de_100_objetos_acoes_plano_trabalho(client):

    mommy.make('PlanoTrabalho', _quantity=101)
    limit_param = '?limit=150'

    url = url_acoesplanotrabalho + limit_param

    request = client.get(url, content_type="application/hal+json")

    assert len(request.data["_embedded"]["items"]) == 100


def test_pesquisa_por_cnpj_prefeitura_em_sistema_de_cultura(client):

    municipio = mommy.make('Municipio', _quantity=2)
    cnpj_param = '?cnpj_prefeitura={}'.format(municipio[0].cnpj_prefeitura)

    url = url_sistemadeculturalocal + cnpj_param

    request = client.get(url, content_type="application/hal+json")

    assert len(request.data["_embedded"]["items"]) == 1
    assert request.data["_embedded"]["items"][0]["ente_federado"]["cnpj_prefeitura"] == municipio[0].cnpj_prefeitura


def test_pesquisa_por_nome_municipio_em_sistema_de_cultura(client):

    cidades = mommy.make('Cidade', _quantity=2)

    for cidade in cidades:
        mommy.make('Municipio', cidade=cidade)

    nome_municipio_param = '?nome_municipio={}'.format(cidades[0].nome_municipio)

    url = url_sistemadeculturalocal + nome_municipio_param

    request = client.get(url, content_type="application/hal+json")

    assert len(request.data["_embedded"]["items"]) == 1
    assert request.data["_embedded"]["items"][0]["ente_federado"]["localizacao"]["cidade"]["nome_municipio"] == cidades[0].nome_municipio

def test_pesquisa_por_nome_municipio_em_sistema_de_cultura_letras_maiusculas(client):

    cidades = mommy.make('Cidade', _quantity=2)

    for cidade in cidades:
        mommy.make('Municipio', cidade=cidade)

    nome_municipio_maiusculo = cidades[0].nome_municipio.upper()
    nome_municipio_param = '?nome_municipio={}'.format(nome_municipio_maiusculo)

    url = url_sistemadeculturalocal + nome_municipio_param

    request = client.get(url, content_type="application/hal+json")

    assert len(request.data["_embedded"]["items"]) == 1
    assert request.data["_embedded"]["items"][0]["ente_federado"]["localizacao"]["cidade"]["nome_municipio"] == cidades[0].nome_municipio

def test_pesquisa_por_nome_municipio_em_sistema_de_cultura_letras_minusculas(client):

    cidades = mommy.make('Cidade', _quantity=2)

    for cidade in cidades:
        mommy.make('Municipio', cidade=cidade)

    nome_municipio_minusculo = cidades[0].nome_municipio.lower()
    nome_municipio_param = '?nome_municipio={}'.format(nome_municipio_minusculo)

    url = url_sistemadeculturalocal + nome_municipio_param

    request = client.get(url, content_type="application/hal+json")

    assert len(request.data["_embedded"]["items"]) == 1
    assert request.data["_embedded"]["items"][0]["ente_federado"]["localizacao"]["cidade"]["nome_municipio"] == cidades[0].nome_municipio


def test_pesquisa_por_nome_uf_em_sistema_de_cultura_letras_maiusculas(client):

    estados = mommy.make('Uf', _quantity=2)

    for estado in estados:
        mommy.make('Municipio', estado=estado)

    nome_uf_maiuscula = estados[0].nome_uf.upper()
    nome_uf_param = '?nome_uf={}'.format(nome_uf_maiuscula)

    url = url_sistemadeculturalocal + nome_uf_param

    request = client.get(url, content_type="application/hal+json")

    assert len(request.data["_embedded"]["items"]) == 1
    assert request.data["_embedded"]["items"][0]["ente_federado"]["localizacao"]["estado"]["nome_uf"] == estados[0].nome_uf


def test_pesquisa_por_nome_uf_em_sistema_de_cultura_letras_minusculas(client):

    estados = mommy.make('Uf', _quantity=2)

    for estado in estados:
        mommy.make('Municipio', estado=estado)

    nome_uf_minuscula = estados[0].nome_uf.lower()
    nome_uf_param = '?nome_uf={}'.format(nome_uf_minuscula)

    url = url_sistemadeculturalocal + nome_uf_param

    request = client.get(url, content_type="application/hal+json")

    assert len(request.data["_embedded"]["items"]) == 1
    assert request.data["_embedded"]["items"][0]["ente_federado"]["localizacao"]["estado"]["nome_uf"] == estados[0].nome_uf

def test_pesquisa_por_estado_sigla_em_sistema_de_cultura(client):

    municipios = mommy.make('Municipio', _quantity=2)

    estado_sigla_param = '?estado_sigla={}'.format(municipios[0].estado.sigla)

    url = url_sistemadeculturalocal + estado_sigla_param

    request = client.get(url, content_type="application/hal+json")

    for municipio in request.data["_embedded"]["items"]:
        assert municipio["ente_federado"]["localizacao"]["estado"]["sigla"] == municipios[0].estado.sigla

def test_pesquisa_por_estado_sigla_minuscula_em_sistema_de_cultura(client):

    municipios = mommy.make('Municipio', _quantity=2)

    estado_sigla_minuscula = municipios[0].estado.sigla.lower()
    estado_sigla_param = '?estado_sigla={}'.format(estado_sigla_minuscula)

    url = url_sistemadeculturalocal + estado_sigla_param

    request = client.get(url, content_type="application/hal+json")

    for municipio in request.data["_embedded"]["items"]:
        assert municipio["ente_federado"]["localizacao"]["estado"]["sigla"] == municipios[0].estado.sigla

def test_pesquisa_por_estado_sigla_maiuscula_em_sistema_de_cultura(client):

    municipios = mommy.make('Municipio', _quantity=2)

    estado_sigla_maiuscula = municipios[0].estado.sigla.upper()
    estado_sigla_param = '?estado_sigla={}'.format(estado_sigla_maiuscula)

    url = url_sistemadeculturalocal + estado_sigla_param

    request = client.get(url, content_type="application/hal+json")

    for municipio in request.data["_embedded"]["items"]:
        assert municipio["ente_federado"]["localizacao"]["estado"]["sigla"] == municipios[0].estado.sigla

def test_pesquisa_por_situacao_adesao_1_em_sistema_de_cultura(client):

    municipios = mommy.make('Municipio', _quantity=2)
    estados_processo = ['1', '2', '3', '4', '5', '6']

    for municipio in municipios:
        mommy.make('Usuario', municipio=municipio,
                   estado_processo=random.choice(estados_processo))

    situacao_adesao_param = '?situacao_adesao=1'
    url = url_sistemadeculturalocal + situacao_adesao_param

    request = client.get(url, content_type="application/hal+json")

    for municipio in request.data["_embedded"]["items"]:
        assert municipio["situacao_adesao"]["situacao_adesao"] == 'Aguardando envio da documentação'


def test_pesquisa_por_situacao_adesao_2_em_sistema_de_cultura(client):

    municipios = mommy.make('Municipio', _quantity=2)
    estados_processo = ['1', '2', '3', '4', '5', '6']

    for municipio in municipios:
        mommy.make('Usuario', municipio=municipio,
                   estado_processo=random.choice(estados_processo))

    situacao_adesao_param = '?situacao_adesao=2'
    url = url_sistemadeculturalocal + situacao_adesao_param

    request = client.get(url, content_type="application/hal+json")

    for municipio in request.data["_embedded"]["items"]:
        assert municipio["situacao_adesao"]["situacao_adesao"] == 'Documentação Recebida - Aguarda Análise'


def test_pesquisa_por_situacao_adesao_3_em_sistema_de_cultura(client):

    municipios = mommy.make('Municipio', _quantity=2)
    estados_processo = ['1', '2', '3', '4', '5', '6']

    for municipio in municipios:
        mommy.make('Usuario', municipio=municipio,
                   estado_processo=random.choice(estados_processo))

    situacao_adesao_param = '?situacao_adesao=3'
    url = url_sistemadeculturalocal + situacao_adesao_param

    request = client.get(url, content_type="application/hal+json")

    for municipio in request.data["_embedded"]["items"]:
        assert municipio["situacao_adesao"]["situacao_adesao"] == 'Diligência Documental'


def test_pesquisa_por_situacao_adesao_4_em_sistema_de_cultura(client):

    municipios = mommy.make('Municipio', _quantity=2)
    estados_processo = ['1', '2', '3', '4', '5', '6']

    for municipio in municipios:
        mommy.make('Usuario', municipio=municipio,
                   estado_processo=random.choice(estados_processo))

    situacao_adesao_param = '?situacao_adesao=4'
    url = url_sistemadeculturalocal + situacao_adesao_param

    request = client.get(url, content_type="application/hal+json")

    for municipio in request.data["_embedded"]["items"]:
        assert municipio["situacao_adesao"]["situacao_adesao"] == 'Encaminhado para assinatura do Secretário SAI'


def test_pesquisa_por_situacao_adesao_5_em_sistema_de_cultura(client):

    municipios = mommy.make('Municipio', _quantity=2)
    estados_processo = ['1', '2', '3', '4', '5', '6']

    for municipio in municipios:
        mommy.make('Usuario', municipio=municipio,
                   estado_processo=random.choice(estados_processo))

    situacao_adesao_param = '?situacao_adesao=5'
    url = url_sistemadeculturalocal + situacao_adesao_param

    request = client.get(url, content_type="application/hal+json")

    for municipio in request.data["_embedded"]["items"]:
        assert municipio["situacao_adesao"]["situacao_adesao"] == 'Aguarda Publicação no DOU'


def test_pesquisa_por_situacao_adesao_6_em_sistema_de_cultura(client):

    municipios = mommy.make('Municipio', _quantity=5)
    estados_processo = ['1', '2', '3', '4', '5', '6']

    for municipio in municipios:
        mommy.make('Usuario', municipio=municipio,
                   estado_processo=random.choice(estados_processo))

    situacao_adesao_param = '?situacao_adesao=6'
    url = url_sistemadeculturalocal + situacao_adesao_param

    request = client.get(url, content_type="application/hal+json")

    for municipio in request.data["_embedded"]["items"]:
        assert municipio["situacao_adesao"]["situacao_adesao"] == 'Publicado no DOU'


def test_pesquisa_data_adesao_sistema_de_cultura(client, plano_trabalho):
    mommy.make('Municipio', _quantity=5)
    sistema_de_cultura = Municipio.objects.first()

    data_param = '?data_adesao={}'.format(sistema_de_cultura.usuario.data_publicacao_acordo)
    url = url_sistemadeculturalocal + data_param

    request = client.get(url, content_type="application/hal+json")

    assert len(request.data["_embedded"]["items"]) == 1
    assert request.data["_embedded"]["items"][0]["data_adesao"] == str(sistema_de_cultura.usuario.data_publicacao_acordo)


def test_pesquisa_range_data_adesao_sistema_de_cultura(client, plano_trabalho):
    municipios = mommy.make('Municipio', _quantity=3)
    sistema_de_cultura = Municipio.objects.first()
    old_date = datetime.date.today() - datetime.timedelta(2)
    actual_date = sistema_de_cultura.usuario.data_publicacao_acordo

    mommy.make('Usuario', municipio=municipios[0],
               data_publicacao_acordo=old_date)

    mommy.make('Usuario', municipio=municipios[1],
               data_publicacao_acordo=actual_date + datetime.timedelta(4))

    mommy.make('Usuario', municipio=municipios[2],
               data_publicacao_acordo=actual_date + datetime.timedelta(5))

    data_range_param = '?data_adesao_min={}&data_adesao_max={}'.format(old_date, actual_date)
    url = url_sistemadeculturalocal + data_range_param

    request = client.get(url, content_type="application/hal+json")

    data = request.data["_embedded"]["items"]

    assert len(data) == 2
    assert data[0]["data_adesao"] == str(old_date)
    assert data[1]["data_adesao"] == str(actual_date)


""" Testa requisição do tipo OPTIONS """


def test_200_options_sistema_de_cultura(client):
    request = client.options(url_sistemadeculturalocal)

    assert request.status_code == 200


def test_choices_ente_federado_sistema_de_cultura(client):
    request = client.options(url_sistemadeculturalocal)

    situacoes_list = []

    for situacao in LISTA_ESTADOS_PROCESSO:
        situacoes_list.append({'id': situacao[0], 'description': situacao[1]})

    assert request.data['ente_federado']['situacao_adesao']['choices'] == situacoes_list


def test_choices_situacao_acoes_plano_trabalho(client):
    request = client.options(url_acoesplanotrabalho)

    situacoes_list = []

    situacoes = SituacoesArquivoPlano.objects.all()

    for situacao in situacoes:
        situacoes_list.append(
            {'id': situacao.id, 'description': situacao.descricao}
            )

    assert request.data['situacao']['choices'] == situacoes_list


def test_choices_segmento_conselheiros(client):
    request = client.options(url_sistemadeculturalocal)

    segments_list = []

    for segmento in SETORIAIS:
        segments_list.append({'id': segmento[0], 'description': segmento[1]})

    assert request.data['conselho']['segmento']['choices'] == segments_list


def test_choices_situacao_conselheiro(client):
    request = client.options(url_sistemadeculturalocal)

    situacao_list = []

    for situacao in SITUACAO_CONSELHEIRO:
        situacao_list.append({'id': situacao[0], 'description': situacao[1]})

    assert request.data['conselho']['situacao']['choices'] == situacao_list


def test_retorno_sistemas_cultura_municipios(client, entes_municipais_estaduais):
    """ Testa retorno de sistema culturas que são referentes a adesões
    de entes federados municipais """
    estado, municipio = entes_municipais_estaduais
    url = url_sistemadeculturalocal + '?municipal=true'

    response = client.get(url)
    municipio_response = response.data['_embedded']['items'][0]['ente_federado']['localizacao']['cidade']['nome_municipio']

    assert len(response.data['_embedded']['items']) == 1
    assert municipio_response == municipio.cidade.nome_municipio


def test_retorno_sistemas_cultura_estados(client, entes_municipais_estaduais):
    """ Testa retorno de sistema culturas que são referentes a adesões
    de entes federados estaduais """

    estadual, municipio = entes_municipais_estaduais
    url = url_sistemadeculturalocal + '?estadual=true'

    response = client.get(url)
    municipio_response = response.data['_embedded']['items'][0]['ente_federado']['localizacao']['estado']['sigla']

    assert len(response.data['_embedded']['items']) == 1
    assert municipio_response == estadual.estado.sigla


def test_retorno_sistemas_cultura_estadual_vazio(client, entes_municipais_estaduais):
    """ Testa retorno dos sistemas cultura ao fornecer o parâmetro estadual vazio """

    estadual, municipal = entes_municipais_estaduais

    url = url_sistemadeculturalocal + '?estadual=&municipal=true'
    response = client.get(url)
    cidade = response.data['_embedded']['items'][0]['ente_federado']['localizacao']['cidade']

    assert len(response.data['_embedded']['items']) == 1
    assert cidade['nome_municipio'] == municipal.cidade.nome_municipio


def test_retorno_sistemas_cultura_municipal_vazio(client, entes_municipais_estaduais):
    """ Testa retorno dos sistemas cultura ao fornecer o parâmetro municipal vazio """

    estadual, municipal = entes_municipais_estaduais

    url = url_sistemadeculturalocal + '?estadual=true&municipal='
    response = client.get(url)
    cidade = response.data['_embedded']['items'][0]['ente_federado']['localizacao']['estado']

    assert len(response.data['_embedded']['items']) == 1
    assert cidade['sigla'] == estadual.estado.sigla


def test_filtrar_por_nome_ente_federado_sigla_estado(client, entes_municipais_estaduais):
    """ Testa retorno de sistemas de cultura passando o nome do ente federado
    como parâmetro, nesse caso a sigla do estado"""

    estadual, municipal = entes_municipais_estaduais
    mommy.make('Municipio')

    url = url_sistemadeculturalocal + '?ente_federado={}'.format(estadual.estado.sigla)

    response = client.get(url)

    assert len(response.data['_embedded']['items']) == 2
    for item in response.data['_embedded']['items']:
        assert item['ente_federado']['localizacao']['estado']['sigla'] == estadual.estado.sigla


def test_filtrar_por_nome_ente_federado_nome_estado(client, sistema_cultura):
    """ Testa retorno de sistemas de cultura passando o nome do ente federado
    como parâmetro, nesse caso o nome do estado"""

    url = url_sistemadeculturalocal + '?ente_federado={}'.format(sistema_cultura.ente_federado.nome)

    response = client.get(url)

    assert len(response.data['_embedded']['items']) == 2
    for item in response.data['_embedded']['items']:
        assert item['ente_federado']['localizacao']['estado']['nome_uf'] == estadual.estado.nome_uf


def test_filtrar_por_nome_ente_federado_nome_municipio(client, sistema_cultura):
    """ Testa retorno de sistemas de cultura passando o nome do ente federado
    como parâmetro, nesse caso a nome do município"""

    municipio = sistema_cultura.ente_federado.nome
    url = url_sistemadeculturalocal + f"?ente_federado={municipio}"

    response = client.get(url)
    municipio_resp = response.data['_embedded']['items'][0]['ente_federado']['localizacao']['cidade']['nome_municipio']

    assert len(response.data['_embedded']['items']) == 1
    assert municipio_resp == municipal.cidade.nome_municipio


def test_filtrar_por_nome_ente_federado_vazio(client):
    """ Testa retorno de sistemas de cultura ao passar o parâmetro vazio """
    mommy.make('Municipio')
    url = url_sistemadeculturalocal + '?ente_federado='

    response = client.get(url)

    assert len(response.data['_embedded']['items']) == 1


def test_counts_com_estado_e_municipio_aderidos(client):
    """ Testa as contagens em uma busca que retorna estado e municipio aderidos"""

    estado = mommy.make('Uf', sigla="TO")
    cidade = mommy.make('Cidade')
    municipio_estado = mommy.make('Municipio', estado=estado)
    municipio_cidade = mommy.make('Municipio', estado=estado, cidade=cidade)

    mommy.make('Usuario', municipio=municipio_estado, estado_processo=6)
    mommy.make('Usuario', municipio=municipio_cidade, estado_processo=6)

    url = url_sistemadeculturalocal + '?ente_federado={}'.format("to")

    response = client.get(url)
    count_municipios = response.data['municipios']
    count_estados = response.data['estados']
    count_municipios_aderidos = response.data['municipios_aderidos']
    count_estados_aderidos = response.data['estados_aderidos']

    assert count_municipios == 1
    assert count_estados == 1
    assert count_municipios_aderidos == 1
    assert count_estados_aderidos == 1


def test_counts_com_estado_e_municipio_não_aderidos(client):
    """ Testa as contagens em uma busca que retorna estado e municipio
    não aderidos"""

    estado = mommy.make('Uf', sigla="TO")
    cidade = mommy.make('Cidade')
    municipio_estado = mommy.make('Municipio', estado=estado)
    municipio_cidade = mommy.make('Municipio', estado=estado, cidade=cidade)

    mommy.make('Usuario', municipio=municipio_estado, estado_processo=1)
    mommy.make('Usuario', municipio=municipio_cidade, estado_processo=1)

    url = url_sistemadeculturalocal + '?ente_federado={}'.format("to")

    response = client.get(url)
    count_municipios = response.data['municipios']
    count_estados = response.data['estados']
    count_municipios_aderidos = response.data['municipios_aderidos']
    count_estados_aderidos = response.data['estados_aderidos']

    assert count_municipios == 1
    assert count_estados == 1
    assert count_municipios_aderidos == 0
    assert count_estados_aderidos == 0


def test_counts_com_apenas_estados_não_aderidos(client):
    """ Testa as contagens em uma busca que retorna estados não aderidos"""

    estado_sp = mommy.make('Uf', nome_uf="Amazonas")
    municipio_estado_sp = mommy.make('Municipio', estado=estado_sp)
    estado_mg = mommy.make('Uf', nome_uf="Acre")
    municipio_estado_mg = mommy.make('Municipio', estado=estado_mg)

    cidade = mommy.make('Cidade')
    municipio_cidade = mommy.make('Municipio', estado=estado_sp, cidade=cidade)

    url = url_sistemadeculturalocal + '?ente_federado=a&municipal=false'

    response = client.get(url)
    count_municipios = response.data['municipios']
    count_estados = response.data['estados']
    count_municipios_aderidos = response.data['municipios_aderidos']
    count_estados_aderidos = response.data['estados_aderidos']

    assert count_municipios == 0
    assert count_estados == 2
    assert count_municipios_aderidos == 0
    assert count_estados_aderidos == 0

def test_counts_com_um_municipio_não_aderido(client):
    """ Testa as contagens em uma busca que retorna um municipio não aderido"""

    estado_sp = mommy.make('Uf', nome_uf="Amazonas")
    municipio_estado_sp = mommy.make('Municipio', estado=estado_sp)
    estado_mg = mommy.make('Uf', nome_uf="Acre")
    municipio_estado_mg = mommy.make('Municipio', estado=estado_mg)

    cidade = mommy.make('Cidade')
    municipio_cidade = mommy.make('Municipio', estado=estado_sp, cidade=cidade)

    url = url_sistemadeculturalocal + '?ente_federado=a&estadual=false'

    response = client.get(url)
    count_municipios = response.data['municipios']
    count_estados = response.data['estados']
    count_municipios_aderidos = response.data['municipios_aderidos']
    count_estados_aderidos = response.data['estados_aderidos']

    assert count_municipios == 1
    assert count_estados == 0
    assert count_municipios_aderidos == 0
    assert count_estados_aderidos == 0


def test_counts_com_apenas_estados_aderidos(client):
    """ Testa as contagens em uma busca que retorna estados aderidos"""

    estado_sp = mommy.make('Uf', nome_uf="Amazonas")
    municipio_estado_sp = mommy.make('Municipio', estado=estado_sp)
    estado_mg = mommy.make('Uf', nome_uf="Acre")
    municipio_estado_mg = mommy.make('Municipio', estado=estado_mg)

    mommy.make('Usuario', municipio=municipio_estado_sp, estado_processo=6)
    mommy.make('Usuario', municipio=municipio_estado_mg, estado_processo=6)

    cidade = mommy.make('Cidade')
    municipio_cidade = mommy.make('Municipio', estado=estado_sp, cidade=cidade)
    mommy.make('Usuario', municipio=municipio_cidade, estado_processo=6)

    url = url_sistemadeculturalocal + '?ente_federado=a&municipal=false'

    response = client.get(url)
    count_municipios = response.data['municipios']
    count_estados = response.data['estados']
    count_municipios_aderidos = response.data['municipios_aderidos']
    count_estados_aderidos = response.data['estados_aderidos']

    assert count_municipios == 0
    assert count_estados == 2
    assert count_municipios_aderidos == 0
    assert count_estados_aderidos == 2

def test_counts_com_um_municipio_aderido(client):
    """ Testa as contagens em uma busca que retorna um municipio aderido"""

    estado_sp = mommy.make('Uf', nome_uf="Amazonas")
    municipio_estado_sp = mommy.make('Municipio', estado=estado_sp)
    estado_mg = mommy.make('Uf', nome_uf="Acre")
    municipio_estado_mg = mommy.make('Municipio', estado=estado_mg)

    mommy.make('Usuario', municipio=municipio_estado_sp, estado_processo=6)
    mommy.make('Usuario', municipio=municipio_estado_mg, estado_processo=6)

    cidade = mommy.make('Cidade')
    municipio_cidade = mommy.make('Municipio', estado=estado_sp, cidade=cidade)
    mommy.make('Usuario', municipio=municipio_cidade, estado_processo=6)

    url = url_sistemadeculturalocal + '?ente_federado=a&estadual=false'

    response = client.get(url)
    count_municipios = response.data['municipios']
    count_estados = response.data['estados']
    count_municipios_aderidos = response.data['municipios_aderidos']
    count_estados_aderidos = response.data['estados_aderidos']

    assert count_municipios == 1
    assert count_estados == 0
    assert count_municipios_aderidos == 1
    assert count_estados_aderidos == 0


def test_ordenar_resultados_da_api_de_forma_ascendente_por_nome_municipio(client):
    """ Testa a ordenação ascendente do resultado da API por cidade(nome_municipio) """

    nomes_municipios = ['Brasilia', 'Zé Doca', 'Abaetetuba']
    
    for nome in nomes_municipios:
        cidade =  mommy.make('Cidade', nome_municipio=nome)
        municipios = mommy.make('Municipio', cidade=cidade)

    url = url_sistemadeculturalocal + '?ordering=cidade__nome_municipio'
    response = client.get(url)

    municipio = response.data['_embedded']['items']

    assert municipio[0]['ente_federado']['localizacao']['cidade']['nome_municipio'] == nomes_municipios[2]
    assert municipio[1]['ente_federado']['localizacao']['cidade']['nome_municipio'] == nomes_municipios[0]
    assert municipio[2]['ente_federado']['localizacao']['cidade']['nome_municipio'] == nomes_municipios[1]

def test_ordenar_resultados_da_api_de_forma_descendente_por_nome_municipio(client):
    """ Testa a ordenação descendente do resultado da API por cidade(nome_municipio) """
    nomes_municipios = ['Brasilia', 'Zé Doca', 'Abaetetuba']
    
    for nome in nomes_municipios:
        cidade =  mommy.make('Cidade', nome_municipio=nome)
        municipios = mommy.make('Municipio', cidade=cidade)

    url = url_sistemadeculturalocal + '?ordering=-cidade__nome_municipio'
    response = client.get(url)

    municipio = response.data['_embedded']['items']
    
    assert municipio[0]['ente_federado']['localizacao']['cidade']['nome_municipio'] == nomes_municipios[1]
    assert municipio[1]['ente_federado']['localizacao']['cidade']['nome_municipio'] == nomes_municipios[0]
    assert municipio[2]['ente_federado']['localizacao']['cidade']['nome_municipio'] == nomes_municipios[2]


def test_ordenar_resultados_da_api_de_forma_ascendente_por_estado(client):
    """ Testa a ordenação ascendente do resultado da API por estado(nome_uf) """
    
    nomes_estados = ['Distrito Federal', 'Bahia', 'Tocantins']
    
    for nome in nomes_estados:
        uf = mommy.make('Uf', nome_uf=nome)
        municipios = mommy.make('Municipio', estado=uf)
        
    url = url_sistemadeculturalocal + '?ordering=estado__nome_uf'
    response = client.get(url)

    estado = response.data['_embedded']['items']

    assert estado[0]['ente_federado']['localizacao']['estado']['nome_uf'] == nomes_estados[1]
    assert estado[1]['ente_federado']['localizacao']['estado']['nome_uf'] == nomes_estados[0]
    assert estado[2]['ente_federado']['localizacao']['estado']['nome_uf'] == nomes_estados[2]



def test_ordenar_resultados_da_api_de_forma_descendente_por_estado(client):
    """ Testa a ordenação descendente do resultado da API por estado(nome_uf) """
    
    nomes_estados = ['Distrito Federal', 'Bahia', 'Tocantins']
    
    for nome in nomes_estados:
        uf = mommy.make('Uf', nome_uf=nome)
        municipios = mommy.make('Municipio', estado=uf)
        
    url = url_sistemadeculturalocal + '?ordering=-estado__nome_uf'

    response = client.get(url)

    estado = response.data['_embedded']['items']

    assert estado[0]['ente_federado']['localizacao']['estado']['nome_uf'] == nomes_estados[2]
    assert estado[1]['ente_federado']['localizacao']['estado']['nome_uf'] == nomes_estados[0]
    assert estado[2]['ente_federado']['localizacao']['estado']['nome_uf'] == nomes_estados[1]
    

@pytest.mark.parametrize("query,componente", [
    ("situacao_lei_id", "criacao_sistema"),
    ("situacao_orgao_id", "orgao_gestor"),
    ("situacao_fundo_id", "fundo_cultura"),
    ("situacao_plano_id", "plano_cultura"),
    ("situacao_conselho_id", "conselho_cultural"),
    ])
def test_filtrar_componente_situacao_id_acoesplanotrabalho(client, plano_trabalho,
                                                           query, componente):
    """ Testa retorno ao filtrar por id do componente do plano de trabalho
    no endpoint acoesplanotrabalho """

    mommy.make('Municipio', _quantity=2)
    situacao = getattr(plano_trabalho, componente).situacao

    url = url_acoesplanotrabalho + '?{}={}'.format(query, situacao.id)

    response = client.get(url)

    assert len(response.data['_embedded']['items']) == 1


@pytest.mark.parametrize("query,componente", [
    ("situacao_lei_descricao", "criacao_sistema"),
    ("situacao_orgao_descricao", "orgao_gestor"),
    ("situacao_fundo_descricao", "fundo_cultura"),
    ("situacao_plano_descricao", "plano_cultura"),
    ("situacao_conselho_descricao", "conselho_cultural"),
    ])
def test_filtrar_componente_situacao_descricao_acoesplanotrabalho(client, plano_trabalho,
                                                                  query, componente):
    """ Testa retorno ao filtrar por descrição componente do plano de trabalho
    no endpoint acoesplanotrabalho """

    mommy.make('Municipio', _quantity=2)
    situacao = getattr(plano_trabalho, componente).situacao

    url = url_acoesplanotrabalho + '?{}={}'.format(query, situacao.descricao)

    response = client.get(url)

    assert len(response.data['_embedded']['items']) == 1


@pytest.mark.parametrize("query,componente", [
    ("situacao_lei_id", "criacao_sistema"),
    ("situacao_orgao_id", "orgao_gestor"),
    ("situacao_fundo_id", "fundo_cultura"),
    ("situacao_plano_id", "plano_cultura"),
    ("situacao_conselho_id", "conselho_cultural"),
    ])
def test_filtra_por_situacao_id_componente_sistema_de_cultura(client, plano_trabalho,
                                                              query, componente):
    """ Testa retorno ao filtrar sistemas de cultura locais por id da situação
    dos componentes do plano de trabalho """

    mommy.make('Municipio', _quantity=2)
    situacao = getattr(plano_trabalho, componente).situacao

    url = url_sistemadeculturalocal + '?{}={}'.format(query, situacao.id)

    response = client.get(url)

    assert len(response.data['_embedded']['items']) == 1


@pytest.mark.parametrize("query,componente", [
    ("situacao_lei_descricao", "criacao_sistema"),
    ("situacao_orgao_descricao", "orgao_gestor"),
    ("situacao_fundo_descricao", "fundo_cultura"),
    ("situacao_plano_descricao", "plano_cultura"),
    ("situacao_conselho_descricao", "conselho_cultural"),
    ])
def test_filtra_por_situacao_descricao_componente_sistema_de_cultura(client,
                                                                     plano_trabalho,
                                                                     query, componente):
    """ Testa retorno ao filtrar sistemas de cultura locais por descrição da situação
    dos componentes do plano de trabalho """

    mommy.make('Municipio', _quantity=2)
    situacao = getattr(plano_trabalho, componente).situacao

    url = url_sistemadeculturalocal + '?{}={}'.format(query, situacao.descricao)

    response = client.get(url)

    assert len(response.data['_embedded']['items']) == 1

def test_filtra_componente_lei_por_multiplos_ids_situacao(client):
    """ Testa retorno ao filtrar sistemas de cultura locais por múltiplos ids da situação
    do componente lei sistema cultura do plano de trabalho """

    usuarios = mommy.make('Usuario', _quantity=2, _fill_optional=['municipio', 'plano_trabalho'])
    usuario_situacao_invalida =  mommy.make('Usuario', _fill_optional=['municipio', 'plano_trabalho'])
    usuario_situacao_invalida.plano_trabalho.criacao_sistema = mommy.make('CriacaoSistema', situacao__id=5)
    usuario_situacao_invalida.plano_trabalho.save()

    for usuario in usuarios:
        criacao_sistema = mommy.make('CriacaoSistema')
        usuario.plano_trabalho.criacao_sistema = criacao_sistema
        usuario.plano_trabalho.save()
    
    usuarios[0].plano_trabalho.criacao_sistema.situacao.id = 1
    usuarios[0].plano_trabalho.criacao_sistema.save()

    url = url_sistemadeculturalocal + '?situacao_lei_id=0&situacao_lei_id=1'

    response = client.get(url)

    assert len(response.data['_embedded']['items']) == 2
    for componentes in response.data['_embedded']['items']:
        situacao = componentes['_embedded']['acoes_plano_trabalho']['criacao_lei_sistema_cultura']['situacao']
        assert situacao == 'Avaliando anexo' or situacao == 'Em preenchimento' 

def test_filtra_componente_conselho_por_multiplos_ids_situacao(client):
    """ Testa retorno ao filtrar sistemas de cultura locais por múltiplos ids da situação
    do componente conselho cultural do plano de trabalho """

    usuarios = mommy.make('Usuario', _quantity=2, _fill_optional=['municipio', 'plano_trabalho'])
    usuario_situacao_invalida =  mommy.make('Usuario', _fill_optional=['municipio', 'plano_trabalho'])
    usuario_situacao_invalida.plano_trabalho.conselho_cultural = mommy.make('ConselhoCultural', situacao__id=5)
    usuario_situacao_invalida.plano_trabalho.save()

    for usuario in usuarios:
        conselho_cultural = mommy.make('ConselhoCultural')
        usuario.plano_trabalho.conselho_cultural = conselho_cultural
        usuario.plano_trabalho.save()
    
    usuarios[0].plano_trabalho.conselho_cultural.situacao.id = 1
    usuarios[0].plano_trabalho.conselho_cultural.save()

    url = url_sistemadeculturalocal + '?situacao_conselho_id=0&situacao_conselho_id=1'

    response = client.get(url)

    assert len(response.data['_embedded']['items']) == 2
    for componentes in response.data['_embedded']['items']:
        situacao = componentes['_embedded']['acoes_plano_trabalho']['criacao_conselho_cultural']['situacao']
        assert situacao == 'Avaliando anexo' or situacao == 'Em preenchimento' 


def test_filtra_componente_fundo_por_multiplos_ids_situacao(client):
    """ Testa retorno ao filtrar sistemas de cultura locais por múltiplos ids da situação
    do componente fundo cultura do plano de trabalho """

    usuarios = mommy.make('Usuario', _quantity=2, _fill_optional=['municipio', 'plano_trabalho'])
    usuario_situacao_invalida =  mommy.make('Usuario', _fill_optional=['municipio', 'plano_trabalho'])
    usuario_situacao_invalida.plano_trabalho.fundo_cultura = mommy.make('FundoCultura', situacao__id=5)
    usuario_situacao_invalida.plano_trabalho.save()

    for usuario in usuarios:
        fundo_cultura = mommy.make('FundoCultura')
        usuario.plano_trabalho.fundo_cultura = fundo_cultura
        usuario.plano_trabalho.save()
    
    usuarios[0].plano_trabalho.fundo_cultura.situacao.id = 1
    usuarios[0].plano_trabalho.fundo_cultura.save()

    url = url_sistemadeculturalocal + '?situacao_fundo_id=0&situacao_fundo_id=1'

    response = client.get(url)

    assert len(response.data['_embedded']['items']) == 2
    for componentes in response.data['_embedded']['items']:
        situacao = componentes['_embedded']['acoes_plano_trabalho']['criacao_fundo_cultura']['situacao']
        assert situacao == 'Avaliando anexo' or situacao == 'Em preenchimento' 

def test_filtra_componente_orgao_por_multiplos_ids_situacao(client):
    """ Testa retorno ao filtrar sistemas de cultura locais por múltiplos ids da situação
    do componente órgão gestor do plano de trabalho """

    usuarios = mommy.make('Usuario', _quantity=2, _fill_optional=['municipio', 'plano_trabalho'])
    usuario_situacao_invalida =  mommy.make('Usuario', _fill_optional=['municipio', 'plano_trabalho'])
    usuario_situacao_invalida.plano_trabalho.orgao_gestor = mommy.make('OrgaoGestor', situacao__id=5)
    usuario_situacao_invalida.plano_trabalho.save()

    for usuario in usuarios:
        orgao_gestor = mommy.make('OrgaoGestor')
        usuario.plano_trabalho.orgao_gestor = orgao_gestor
        usuario.plano_trabalho.save()
    
    usuarios[0].plano_trabalho.orgao_gestor.situacao.id = 1
    usuarios[0].plano_trabalho.orgao_gestor.save()

    url = url_sistemadeculturalocal + '?situacao_orgao_id=0&situacao_orgao_id=1'

    response = client.get(url)

    assert len(response.data['_embedded']['items']) == 2
    for componentes in response.data['_embedded']['items']:
        situacao = componentes['_embedded']['acoes_plano_trabalho']['criacao_orgao_gestor']['situacao']
        assert situacao == 'Avaliando anexo' or situacao == 'Em preenchimento' 

def test_filtra_componente_plano_por_multiplos_ids_situacao(client):
    """ Testa retorno ao filtrar sistemas de cultura locais por múltiplos ids da situação
    do componente plano cultura do plano de trabalho """

    usuarios = mommy.make('Usuario', _quantity=2, _fill_optional=['municipio', 'plano_trabalho'])
    usuario_situacao_invalida =  mommy.make('Usuario', _fill_optional=['municipio', 'plano_trabalho'])
    usuario_situacao_invalida.plano_trabalho.plano_cultura = mommy.make('PlanoCultura', situacao__id=5)
    usuario_situacao_invalida.plano_trabalho.save()

    for usuario in usuarios:
        plano_cultura = mommy.make('PlanoCultura')
        usuario.plano_trabalho.plano_cultura = plano_cultura
        usuario.plano_trabalho.save()
    
    usuarios[0].plano_trabalho.plano_cultura.situacao.id = 1
    usuarios[0].plano_trabalho.plano_cultura.save()

    url = url_sistemadeculturalocal + '?situacao_plano_id=0&situacao_plano_id=1'

    response = client.get(url)

    assert len(response.data['_embedded']['items']) == 2
    for componentes in response.data['_embedded']['items']:
        situacao = componentes['_embedded']['acoes_plano_trabalho']['criacao_plano_cultura']['situacao']
        assert situacao == 'Avaliando anexo' or situacao == 'Em preenchimento' 


def test_pesquisa_por_nome_municipio_para_municipios_com_acento_no_nome(client):
    ''' Pesquisa (sem acento) o nome de um municpio que tenha acento - Deve retornar normalmente'''
    mommy.make('Municipio', cidade=mommy.make('Cidade', nome_municipio='Acrelândia'))

    nome_municipio_param = '?nome_municipio={}'.format('Acrelandia')

    url = url_sistemadeculturalocal + nome_municipio_param

    request = client.get(url, content_type="application/hal+json")
    assert len(request.data["_embedded"]["items"]) == 1
    assert request.data["_embedded"]["items"][0]["ente_federado"]["localizacao"]["cidade"]["nome_municipio"] == 'Acrelândia'

def test_pesquisa_por_nome_estado_para_estados_com_acento_no_nome(client):
    ''' Pesquisa (sem acento) o nome de um municpio que tenha acento - Deve retornar normalmente'''
    mommy.make('Municipio', estado=mommy.make('Uf', nome_uf='Goiás'))

    nome_municipio_param = '?nome_uf={}'.format('Goias')

    url = url_sistemadeculturalocal + nome_municipio_param

    request = client.get(url, content_type="application/hal+json")
    assert request.data["_embedded"]["items"][0]["ente_federado"]["localizacao"]['estado']['nome_uf'] == 'Goiás'
