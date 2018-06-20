import pytest

from model_mommy import mommy

from adesao.models import SistemaCultura
from adesao.models import Usuario


@pytest.mark.xfail
def test_existe_um_model_SistemaCultura():

    with pytest.raises(ImportError):
        from adesao.models import SistemaCultura


def test_atributo_cadastrador_de_um_SistemaCultura():

    sistema = SistemaCultura()

    assert sistema._meta.get_field('cadastrador')


def test_atributo_cidade_de_um_SistemaCultura():

    sistema = SistemaCultura()

    assert sistema._meta.get_field('cidade')


def test_atributo_uf_de_um_SistemaCultura():

    sistema = SistemaCultura()

    assert sistema._meta.get_field('uf')


# def test_alterar_cadastrador_SistemaCultura(plano_trabalho):
#     """ Testa método alterar_cadastrador da model SistemaCultura"""

#     cadastrador_atual = Usuario.objects.first()
#     ente_federado = cadastrador_atual.municipio
#     plano_trabalho = cadastrador_atual.plano_trabalho
#     secretario = cadastrador_atual.secretario
#     responsavel = cadastrador_atual.responsavel
#     uf = ente_federado.estado
#     user = mommy.make('Usuario')

#     sistema = SistemaCultura(uf=uf, cadastrador=user)
#     sistema.save()
#     sistema.alterar_cadastrador(user, cadastrador_atual)
#     assert SistemaCultura.objects.all().count() == 1
#     assert ente_federado.usuario == user
#     assert plano_trabalho.usuario == user
#     assert secretario.usuario == user
#     assert responsavel.usuario == user
#     assert user.data_publicacao_acordo == cadastrador_atual.data_publicacao_acordo
#     assert user.estado_processo == cadastrador_atual.estado_processo

