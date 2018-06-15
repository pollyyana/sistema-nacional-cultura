import pytest

from django.shortcuts import reverse
from dal.autocomplete import ModelSelect2

from adesao.forms import CadastrarMunicipioForm
from adesao.models import Usuario


@pytest.fixture
def cadastrar_municipio_form(login):
    user = Usuario.objects.first()
    kwargs = {'user': user}
    return CadastrarMunicipioForm(**kwargs)


def test_widget_estado_form_cadastrar_municipio(client, cadastrar_municipio_form):
    """
    Testa o uso do widget ModelSelect2 na campo estado no form de
    cadastrar município
    """

    form = cadastrar_municipio_form
    assert isinstance(form['estado'].field.widget, ModelSelect2)


def test_url_widget_estado_form_cadastrar_municipio(client, cadastrar_municipio_form):
    """
    Testa url usada pelo widget ModelSelect2 no campo estado no form
    de cadastrar municipio
    """

    form = cadastrar_municipio_form
    uf_url = reverse('gestao:uf_chain')

    assert form['estado'].field.widget.url == uf_url


def test_widget_cidade_form_cadastrar_municipio(client, cadastrar_municipio_form):
    """
    Testa o uso do widget ModelSelect2 no campo cidade no form de
    cadastrar municipio
    """

    form = cadastrar_municipio_form
    assert isinstance(form['cidade'].field.widget, ModelSelect2)


def test_url_widget_cidade_form_cadastrar_municipio(client, cadastrar_municipio_form):
    """
    Testa url usada pelo widget ModelSelect2 no campo cidade no
    form de cadastrar municipio
    """

    form = cadastrar_municipio_form
    municipio_url = reverse('gestao:cidade_chain')
    assert form['cidade'].field.widget.url == municipio_url
