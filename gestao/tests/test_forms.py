import pytest
from django.forms import ModelForm
from django.shortcuts import reverse

from gestao.forms import DiligenciaComponenteForm, DiligenciaGeralForm
from gestao.models import DiligenciaSimples

from ckeditor.widgets import CKEditorWidget
from dal.autocomplete import ModelSelect2
from model_mommy import mommy

from gestao.forms import AlterarCadastradorForm

pytestmark = pytest.mark.django_db


def test_existencia_form_diligencia_componente(client, login, sistema_cultura):
    """ Testa existência da classe form para a diligência de componentes"""

    form = DiligenciaComponenteForm(componente='orgao_gestor', sistema_cultura=sistema_cultura,
        usuario=login)

    assert form


def test_existencia_form_diligencia_geral(client, login, sistema_cultura):
    """ Testa existência da classe form para a diligência geral"""

    form = DiligenciaGeralForm(sistema_cultura=sistema_cultura, usuario=login)

    assert form


def test_campo_texto_diligencia_form_componente(client, login, sistema_cultura):
    """
    Testa existência do campo texto_diligência no form referente a diligência de componente
    """

    form = DiligenciaComponenteForm(componente='orgao_gestor', sistema_cultura=sistema_cultura,
        usuario=login)

    assert "<textarea cols=\"40\" id=\"id_texto_diligencia\" name=\"texto_diligencia\" " in form.as_p()


def test_campo_texto_diligencia_form_geral(client, login, sistema_cultura):
    """
    Testa existência do campo texto_diligência no form referente a diligência geral
    """

    form = DiligenciaGeralForm(sistema_cultura=sistema_cultura, usuario=login)
    
    assert "<textarea cols=\"40\" id=\"id_texto_diligencia\" name=\"texto_diligencia\" " in form.as_p()


def test_campo_classificao_arquivo_no_form_diligencia_componente(client, login, sistema_cultura):
    """ Testa a existência do campo referente a seleção para a classificação do arquivo """

    form = DiligenciaComponenteForm(componente='orgao_gestor', sistema_cultura=sistema_cultura,
        usuario=login)

    assert "<select name=\"classificacao_arquivo\" id=\"id_classificacao_arquivo\"" in form.as_p()


def test_ausencia_campo_classificao_arquivo_no_form_diligencia_geral(client, login, sistema_cultura):
    """ Testa se o campo referente a seleção para a classificação do arquivo
    não é disonível na diligência geral """

    form = DiligenciaGeralForm(sistema_cultura=sistema_cultura, usuario=login)

    assert "<select name=\"classificacao_arquivo\" id=\"id_classificacao_arquivo\"" not in form.as_p()


def test_uso_ck_widget_no_texto_diligencia_geral(client, login, sistema_cultura):
    """ Testa uso do widget ckeditor para input de texto rich no texto_diligência """

    form = DiligenciaGeralForm(sistema_cultura=sistema_cultura, usuario=login)

    assert isinstance(form.fields['texto_diligencia'].widget, CKEditorWidget)


def test_validacao_de_dados_invalidos(client, login, sistema_cultura):
    """ Testa se a função is_valid retorna falso para dados inválidos na criação do form 
    da diligencia de componente"""

    data = {'texto_diligencia': 'ta certo, parceiro', 'classificacao_arquivo': 'bla'}

    form = DiligenciaComponenteForm(data=data, componente='orgao_gestor', 
        sistema_cultura=sistema_cultura, usuario=login)

    assert not form.is_valid()


def test_tipo_do_form_da_diligencia_geral(client):
    """ Testa se o form da diligência geral é do tipo ModelForm """

    assert issubclass(DiligenciaGeralForm, ModelForm)


def test_tipo_do_form_da_diligencia_componente(client):
    """ Testa se o form da diligência de componente é do tipo ModelForm """

    assert issubclass(DiligenciaComponenteForm, ModelForm)


def test_diligencia_form_componente_usa_model_correta(client, login, sistema_cultura):
    """ Testa de a classe DiligenciaForm utiliza a model referente a Diligencia """

    form = DiligenciaComponenteForm(componente='orgao_gestor', 
        sistema_cultura=sistema_cultura, usuario=login)

    assert isinstance(form.instance, DiligenciaSimples)


def test_diligencia_form_geral_usa_model_correta(client, login, sistema_cultura):
    """ Testa de a classe DiligenciaForm utiliza a model referente a Diligencia """

    form = DiligenciaGeralForm(sistema_cultura=sistema_cultura, usuario=login)

    assert isinstance(form.instance, DiligenciaSimples)


def test_fields_form_diligencia_componente(client, login, sistema_cultura):
    """Testa as fields dentro do form de diligencia de componente"""

    form = DiligenciaComponenteForm(componente='orgao_gestor', 
        sistema_cultura=sistema_cultura, usuario=login)

    fields = ('texto_diligencia', 'classificacao_arquivo')

    assert set(form.Meta.fields).issuperset(set(fields))


def test_fields_form_diligencia_geral(client, login, sistema_cultura):
    """Testa as fields dentro do form de diligencia geral"""

    form = DiligenciaGeralForm(sistema_cultura=sistema_cultura, usuario=login)
    
    fields = ('texto_diligencia',)

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

    form = AlterarCadastradorForm()
    fields = ("cpf_usuario", "data_publicacao_acordo")

    assert set(form.Meta.fields) == set(fields)


def test_save_alterar_cadastrador_form_com_sistemacultura(sistema_cultura, login):
    """
    Método save do form AlterarCadastradorForm altera as informações necessárias,
    quando um ente fedarado já possui um SistemaCultura associado
    """

    data = {'cpf_usuario': login.user.username}

    form = AlterarCadastradorForm(data=data)
    form.is_valid()
    form.save()

    sistema_cultura.refresh_from_db()

    assert sistema_cultura.cadastrador == login