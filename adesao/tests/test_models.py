import pytest
from datetime import datetime

from django.utils import timezone
from model_mommy import mommy

from adesao.models import SistemaCultura
from adesao.models import Usuario
from adesao.models import Municipio
from adesao.models import Secretario
from adesao.models import Responsavel
from adesao.models import SistemaCulturaManager
from planotrabalho.models import PlanoTrabalho


@pytest.mark.xfail
def test_existe_um_model_SistemaCultura():

    with pytest.raises(ImportError):
        from adesao.models import SistemaCultura


def test_atributo_cadastrador_de_um_SistemaCultura():

    sistema = SistemaCultura()

    assert sistema._meta.get_field("cadastrador")


def test_atributo_cidade_de_um_SistemaCultura():

    sistema = SistemaCultura()

    assert sistema._meta.get_field("cidade")


def test_atributo_uf_de_um_SistemaCultura():

    sistema = SistemaCultura()

    assert sistema._meta.get_field("uf")


def test_atributo_data_criacao_de_um_SistemaCultura():

    sistema = SistemaCultura()

    assert sistema._meta.get_field('data_criacao')


def test_timezone_now_data_criacao_SistemaCultura():

    sistema = SistemaCultura()

    assert sistema.data_criacao.replace(second=0, microsecond=0) ==\
        timezone.now().replace(second=0, microsecond=0)


def test_SistemaCultura_save_cria_nova_instancia():
    """
    SistemaCultura deve sempre retornar uma nova instancia quando da tentativa
    de salvar os dados de uma instancia existente.
    """

    sistema = mommy.make("SistemaCultura", _fill_optional=['cidade', 'uf',
                                                           'cadastrador'])
    user = mommy.make("Usuario")

    sistema.cadastrador = user
    sistema.save()

    assert SistemaCultura.objects.count() == 2

    user.delete()
    [sistema.delete() for sistema in SistemaCultura.objects.all()]


def test_alterar_cadastrador_SistemaCultura(plano_trabalho):
    """ Testa método alterar_cadastrador da model SistemaCultura"""

    cadastrador_atual = plano_trabalho.usuario
    uf = cadastrador_atual.municipio.estado
    user = mommy.make("Usuario")
    sistema = mommy.make("SistemaCultura", cadastrador=cadastrador_atual, uf=uf)

    sistema.cadastrador = user
    sistema.save()

    assert SistemaCultura.objects.count() == 2
    assert Municipio.objects.first().usuario == user
    assert PlanoTrabalho.objects.first().usuario == user
    assert Secretario.objects.first().usuario == user
    assert Responsavel.objects.first().usuario == user
    assert (
        sistema.cadastrador.data_publicacao_acordo
        == cadastrador_atual.data_publicacao_acordo
    )
    assert sistema.cadastrador.estado_processo == cadastrador_atual.estado_processo

    sistema.delete()
    user.delete()


@pytest.mark.skip
def test_limpa_cadastrador_alterado_SistemaCultura():
    """ Testa método para limpar referências de um cadastrador para os outos
    componentes do sistema de adesão """

    cadastrador = mommy.make(
        "Usuario",
        _fill_optional=["secretario", "responsavel", "plano_trabalho", "municipio"],
    )

    cadastrador.limpa_cadastrador()

    assert cadastrador.plano_trabalho is None
    assert cadastrador.municipio is None
    assert cadastrador.secretario is None
    assert cadastrador.responsavel is None
    # assert cadastrador.user.is_active is False

    cadastrador.secretario.delete()
    cadastrador.responsavel.delete()
    cadastrador.plano_trabalho.delete()
    cadastrador.municipio.delete()


def test_manager_usado_SistemaCultura():
    """ Testa se a model SistemaCultura utiliza o manager correto """

    assert isinstance(SistemaCultura.objects.db_manager(), SistemaCulturaManager)


def test_retorna_ativo_SistemaCultura_filtrado_por_uf():
    """ Retorna o último Sistema cultura criado sendo ele o ativo de
    uma UF específica """

    mommy.make('SistemaCultura',
               data_criacao=datetime(2018, 2, 3, 0, tzinfo=timezone.utc),
               _fill_optional=['uf'])
    sistema_ativo = mommy.make('SistemaCultura', _fill_optional=['uf'])

    assert SistemaCultura.objects.ativo(uf=sistema_ativo.uf) == sistema_ativo

    SistemaCultura.objects.all().delete()


def test_retorna_ativo_SistemaCultura_filtrado_por_uf_e_cidade():
    """ Retorna o último Sistema cultura criado sendo ele o ativo de uma
    UF e cidade específicas """

    mommy.make('SistemaCultura',
               data_criacao=datetime(2018, 2, 3, 0, tzinfo=timezone.utc),
               _fill_optional=['uf', 'cidade'])
    sistema_ativo = mommy.make('SistemaCultura', _fill_optional=['uf', 'cidade'])

    assert SistemaCultura.objects.ativo(
            uf=sistema_ativo.uf, cidade=sistema_ativo.cidade) == sistema_ativo


def test_ativo_ou_cria_SistemaCultura_ativo():
    """ Testa método ativo_ou_cria do manager SistemaCulturaManager
    retorna SistemaCultura ativo """

    mommy.make('SistemaCultura',
               data_criacao=datetime(2018, 2, 3, 0, tzinfo=timezone.utc),
               _fill_optional=['uf', 'cidade'])
    sistema_ativo = mommy.make('SistemaCultura', _fill_optional=['uf', 'cidade'])

    assert SistemaCultura.objects.ativo_ou_cria(
            uf=sistema_ativo.uf, cidade=sistema_ativo.cidade) == sistema_ativo


def test_ativo_ou_cria_SistemaCultura_cria():
    """ Testa método ativo_ou_cria do manager SistemaCulturaManager
    retorna um novo sistema cultura """
    cidade = mommy.make('Cidade')
    uf = cidade.uf

    sistema = SistemaCultura.objects.ativo_ou_cria(cidade=cidade, uf=uf)

    assert isinstance(sistema, SistemaCultura)
    assert sistema.pk
    assert sistema.uf == uf
    assert sistema.cidade == cidade


def test_alterar_cadastrador_sistema_cultura_sem_cadastrador():
    """ Testa alterar o cadastrador de um sistema cultura que não possui um
    cadastrador """
    sistema = mommy.make('SistemaCultura')
    cadastrador = mommy.make('Usuario')

    sistema.cadastrador = cadastrador
    sistema.save()
    sistema.refresh_from_db()

    assert sistema.cadastrador == cadastrador
