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

    entidades = ["governo","ente_federado", "conselho", "_embedded","situacao_adesao"]

    for entidade in entidades:
        assert entidade in request.data


def test_campos_do_objeto_governo_ao_retornar_sistema_cultura_local(client):

    municipio = mommy.make('Municipio')

    url = '/v1/sistemadeculturalocal/{}/'.format(municipio.id)
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
                         content_type="application/hal+json")

    campos = set(["nome_prefeito", "email_institucional_prefeito",
                  "termo_posse_prefeito"])

    assert campos.issubset(request.data["governo"])


def test_campos_do_objeto_ente_federado_ao_retornar_sistema_cultura_local(client):

    municipio = mommy.make('Municipio')

    url = '/v1/sistemadeculturalocal/{}/'.format(municipio.id)
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
            content_type="application/hal+json")

    campos = set(["cnpj_prefeitura","endereco_eletronico","telefones","localizacao"])

    assert campos.issubset(request.data["ente_federado"])


def test_campos_do_objeto_embedded_ao_retornar_sistema_cultura_local(client):

    municipio = mommy.make('Municipio')

    url = '/v1/sistemadeculturalocal/{}/'.format(municipio.id)
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
            content_type="application/hal+json")

    campos = set(["acoes_plano_trabalho"])

    assert campos.issubset(request.data["_embedded"])


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

    assert campos.issubset(request.data["conselho"])


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

    plano = mommy.make('PlanoTrabalho')

    url = '/v1/acoesplanotrabalho/{}/'.format(plano.id)
    host_request = 'api'

    request = client.get(url, HTTP_HOST=host_request,
            content_type="application/hal+json")

    assert request.status_code == status.HTTP_200_OK
    assert request.data["id"] == plano.id
