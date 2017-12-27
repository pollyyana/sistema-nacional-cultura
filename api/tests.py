import pytest

from rest_framework import status

from model_mommy import mommy

pytestmark = pytest.mark.django_db

def test_municipios_list_endpoint_returning_200_OK(client):

    url = '/v1/sistemadeculturalocal/'
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request)

    assert request.status_code == status.HTTP_200_OK


def test_URL_sistema_cultura_local_retorna_10_sistemas(client):

    url = '/v1/sistemadeculturalocal/'
    host_request = 'api'

    sistemas = mommy.make('Municipio', _quantity=12)

    request = client.get(url, HTTP_HOST=host_request,
                         content_type="application/hal+json")

    assert isinstance(request.data["_embedded"]["items"], list)
    assert len(request.data["_embedded"]["items"]) == 10


def test_404_recupera_ID_sistema_cultura_local(client):

    url = '/v1/sistemadeculturalocal/45/'
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
                        content_type="application/hal+json")

    assert request.status_code == status.HTTP_404_NOT_FOUND


def test_recupera_ID_param_sistema_cultura_local(client):

    municipio = mommy.make('Municipio')

    url = '/v1/sistemadeculturalocal/{}/'.format(municipio.id)
    host_request = 'api'


    request = client.get(url, HTTP_HOST=host_request,
                        content_type="application/hal+json")

    assert request.status_code == status.HTTP_200_OK
    assert request.data["id"] == municipio.id


def test_entidades_principais_sistema_cultura_local(client):

    municipio = mommy.make('Municipio')

    url = '/v1/sistemadeculturalocal/{}/'.format(municipio.id)
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request, content_type="application/hal+json")

    entidades = set(["governo","ente_federado", "conselho",
        "_embedded","situacao_adesao","_links","id"])

    assert entidades.symmetric_difference(request.data) == set()


def test_campos_do_objeto_governo_ao_retornar_sistema_cultura_local(client):

    municipio = mommy.make('Municipio')

    url = '/v1/sistemadeculturalocal/{}/'.format(municipio.id)
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
                         content_type="application/hal+json")

    campos = set(["nome_prefeito", "email_institucional_prefeito",
                  "termo_posse_prefeito"])

    assert campos.symmetric_difference(request.data["governo"]) == set()


def test_campos_do_objeto_ente_federado_ao_retornar_sistema_cultura_local(client):

    municipio = mommy.make('Municipio')

    url = '/v1/sistemadeculturalocal/{}/'.format(municipio.id)
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
            content_type="application/hal+json")

    campos = set(["cnpj_prefeitura","endereco_eletronico","telefones","localizacao"])

    assert campos.symmetric_difference(request.data["ente_federado"]) == set()


def test_campos_do_objeto_embedded_ao_retornar_sistema_cultura_local(client):

    municipio = mommy.make('Municipio')

    url = '/v1/sistemadeculturalocal/{}/'.format(municipio.id)
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
            content_type="application/hal+json")

    campos = set(["acoes_plano_trabalho"])

    assert campos.symmetric_difference(request.data["_embedded"]) == set()


def test_campos_do_objeto_conselho_ao_retornar_sistema_cultura_local(client):

    municipio = mommy.make('Municipio')
    conselho_cultural= mommy.make('ConselhoCultural')
    plano_trabalho = mommy.make('PlanoTrabalho',conselho_cultural=conselho_cultural)
    usuario = mommy.make('Usuario',municipio=municipio,plano_trabalho=plano_trabalho)
    conselheiro = mommy.make('Conselheiro',conselho=conselho_cultural)

    url = '/v1/sistemadeculturalocal/{}/'.format(municipio.id)
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
            content_type="application/hal+json")

    campos = set(["conselheiros"])

    assert campos.symmetric_difference(request.data["conselho"]) == set()


def test_planotrabalho_list_endpoint_returning_200_OK(client):

    url = '/v1/acoesplanotrabalho/'
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request)

    assert request.status_code == status.HTTP_200_OK


def test_planotrabalho_list_retorna_lista_com_10(client):

    planos = mommy.make('PlanoTrabalho',13)
    url = '/v1/acoesplanotrabalho/'
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
            content_type="application/hal+json")

    assert isinstance(request.data["_embedded"]["items"], list) 
    assert len(request.data["_embedded"]["items"]) == 10


def test_acoesplanotrabalho_retorna_404_para_id_nao_valido(client):

    url = '/v1/acoesplanotrabalho/55/'
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
            content_type="application/hal+json")

    assert request.status_code == status.HTTP_404_NOT_FOUND


def test_acoesplanotrabalho_retorna_para_id_valido(client):

    plano_trabalho = mommy.make('PlanoTrabalho')

    url = '/v1/acoesplanotrabalho/{}/'.format(plano_trabalho.id)
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
            content_type="application/hal+json")

    assert request.status_code == status.HTTP_200_OK
    assert request.data["id"] == plano_trabalho.id


def test_campos_acoesplanotrabalho(client):

    plano_trabalho = mommy.make('PlanoTrabalho')

    url = '/v1/acoesplanotrabalho/{}/'.format(plano_trabalho.id)
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
            content_type="application/hal+json")

    campos = set(["criacao_lei_sistema_cultura","criacao_orgao_gestor",
        "criacao_plano_cultura","criacao_fundo_cultura","criacao_conselho_cultural",
        "_links","id"])

    assert campos.symmetric_difference(request.data) == set()


def test_objeto_criacao_lei_sistema_cultura_acoesplanotrabalho(client):

    criacao_sistema = mommy.make('CriacaoSistema')
    plano_trabalho = mommy.make('PlanoTrabalho',criacao_sistema=criacao_sistema)

    url = '/v1/acoesplanotrabalho/{}/'.format(plano_trabalho.id)
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
            content_type="application/hal+json")

    campos = set(["lei_sistema_cultura","situacao"])

    assert campos.symmetric_difference(request.data["criacao_lei_sistema_cultura"]) == set()


def test_objeto_criacao_orgao_gestor_acoesplanotrabalho(client):

    orgao_gestor = mommy.make('OrgaoGestor')
    plano_trabalho = mommy.make('PlanoTrabalho',orgao_gestor=orgao_gestor)

    url = '/v1/acoesplanotrabalho/{}/'.format(plano_trabalho.id)
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
            content_type="application/hal+json")

    campos = set(["relatorio_atividade_secretaria","situacao"])

    assert campos.symmetric_difference(request.data["criacao_orgao_gestor"]) == set()


def test_objeto_criacao_plano_cultura_acoesplanotrabalho(client):

    plano_cultura= mommy.make('PlanoCultura')
    plano_trabalho = mommy.make('PlanoTrabalho',plano_cultura=plano_cultura)

    url = '/v1/acoesplanotrabalho/{}/'.format(plano_trabalho.id)
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
            content_type="application/hal+json")

    campos = set(["relatorio_diretrizes_aprovadas","minuta_preparada",
        "ata_reuniao_aprovacao_plano","ata_votacao_projeto_lei",
        "lei_plano_cultura","situacao"])

    assert campos.symmetric_difference(request.data["criacao_plano_cultura"]) == set()


def test_objeto_criacao_fundo_cultura_acoesplanotrabalho(client):

    fundo_cultura = mommy.make('FundoCultura')
    plano_trabalho = mommy.make('PlanoTrabalho',fundo_cultura=fundo_cultura)

    url = '/v1/acoesplanotrabalho/{}/'.format(plano_trabalho.id)
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
            content_type="application/hal+json")

    campos = set(["cnpj_fundo_cultura","lei_fundo_cultura","situacao"])

    assert campos.symmetric_difference(request.data["criacao_fundo_cultura"]) == set()


def test_objeto_criacao_conselho_cultural_acoesplanotrabalho(client):

    conselho_cultural = mommy.make('ConselhoCultural')
    plano_trabalho = mommy.make('PlanoTrabalho',conselho_cultural=conselho_cultural)

    url = '/v1/acoesplanotrabalho/{}/'.format(plano_trabalho.id)
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
            content_type="application/hal+json")

    campos = set(["ata_regimento_aprovado","situacao"])

    assert campos.symmetric_difference(request.data["criacao_conselho_cultural"]) == set()


def test_retorno_maximo_de_100_objetos_sistema_de_cultura(client):

    municipio = mommy.make('Municipio',150)
    limit_param = 'limit=150'

    url = '/v1/sistemadeculturalocal/?{}'.format(limit_param)
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
            content_type="application/hal+json")

    assert len(request.data["_embedded"]["items"]) == 100


def test_retorno_maximo_de_100_objetos_acoes_plano_trabalho(client):

    municipio = mommy.make('PlanoTrabalho',150)
    limit_param = 'limit=150'

    url = '/v1/acoesplanotrabalho/?{}'.format(limit_param)
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
            content_type="application/hal+json")

    assert len(request.data["_embedded"]["items"]) == 100
