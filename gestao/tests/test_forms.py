import pytest
from django.forms import ModelForm

from gestao.forms import DiligenciaForm, InserirSEI
from gestao.models import Diligencia

from ckeditor.widgets import CKEditorWidget


pytestmark = pytest.mark.django_db

def test_existencia_form_sei(client):

    """ Testa existência da classe form para a inserção do sei """
    form = InserirSEI()
    assert form

def test_campo_processo_sei_form(client):
    """
    Testa existência do processo_sei no form
    """
    form = InserirSEI()
    assert "<input id=\"id_processo_sei\" maxlength=\"50\" name=\"processo_sei\" type=\"text\"" in form.as_p()

def test_existencia_form_diligencia(client):

    """ Testa existência da classe form para a diligência """
    form = DiligenciaForm(resultado='0', componente='1')
    assert form

def test_campo_texto_diligencia_form(client):
    """
    Testa existência do campo texto_diligência no form referente a diligência
    """
    form = DiligenciaForm(resultado='0', componente='1')
    assert "<textarea cols=\"40\" id=\"id_texto_diligencia\" name=\"texto_diligencia\" " in form.as_p()


def test_campo_classificao_arquivo_no_form_diligencia(client):
    """ Testa a existência do campo referente a seleção para a classificação do arquivo """

    form = DiligenciaForm(resultado='0', componente='1')
    assert "<select name=\"classificacao_arquivo\" id=\"id_classificacao_arquivo\"" in form.as_p()


def test_uso_ck_widget_no_texto_diligencia(client):
    """ Testa uso do widget ckeditor para input de texto rich no texto_diligência """

    form = DiligenciaForm(resultado='0', componente='1')
    assert isinstance(form.fields['texto_diligencia'].widget, CKEditorWidget)


def test_validacao_de_dados_invalidos(client):
    """ Testa se a função is_valid retorna falso para dados inválidos na criação do form """

    data = {'texto_diligencia': 'ta certo, parceiro', 'classificacao_arquivo': 'bla'}

    form = DiligenciaForm(data=data, resultado='0', componente='1')

    assert not form.is_valid()


def test_tipo_do_form_da_diligencia(client):
    """ Testa se o form da Diligência é do tipo ModelForm """

    assert issubclass(DiligenciaForm, ModelForm)


def test_diligencia_form_usa_model_correta(client):
    """ Testa de a classe DiligenciaForm utiliza a model referente a Diligencia """

    form = DiligenciaForm(resultado='0', componente='1')

    assert isinstance(form.instance, Diligencia)


def test_fields_form_diligencia(client):
    """Testa as fields dentro do form Diligencia"""

    form = DiligenciaForm(resultado='0', componente='1')
    fields = ('texto_diligencia', 'classificacao_arquivo')

    assert set(form.Meta.fields).issuperset(set(fields))


@pytest.mark.xfail(strict=True)
def test_form_altera_cadastrador(client):
    """
    Testa a existencia de um formulário para alterar o cadastrador de uma
    adesão.
    """

    with pytest.raises(ImportError) as exception:
        from gestao.forms import AlterarCadastradorForm


def test_campos_form_altera_cadastrador(client):
    """
    Testa a presença dos campos "CPF", "uf", e "Municipio" no formulário para
    alterar o cadastrador de uma adesão.
    """

    from gestao.forms import AlterarCadastradorForm

    form = AlterarCadastradorForm()
    fields = ("cpf_usuario", "uf", "municipio", "data_publicacao_acordo")

    assert set(form.Meta.fields) == set(fields)


# def test_campos_form_retona_todas_uf(client):
#     """
#     Testa se o campo UF retorna todas as UF do país.
#     """

#     from gestao.forms import AlterarCadastradorForm

#     form = AlterarCadastradorForm()

#     __import__('ipdb').set_trace()

def test_aaaaa(rf):

    from gestao.views import AlterarCadastrador
    from model_mommy import mommy

    from django.urls import reverse


    mg = mommy.make('Uf', sigla_uf='MG')

    url = reverse('gestao:municipio_chain')
    request = rf.get(url)
    __import__('ipdb').set_trace()