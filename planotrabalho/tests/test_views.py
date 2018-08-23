import pytest

from django.urls import reverse
from django.urls import resolve
from django.core.files.uploadedfile import SimpleUploadedFile

from model_mommy import mommy


@pytest.mark.parametrize(
    "url, componente",
    [
        (reverse("planotrabalho:cadastrar_sistema"), "criacao_sistema"),
        (reverse("planotrabalho:gestor"), "orgao_gestor"),
        (reverse("planotrabalho:conselho"), "conselho_cultural"),
        (reverse("planotrabalho:fundo"), "fundo_cultura"),
        (reverse("planotrabalho:plano"), "plano_cultura"),
    ],
)
def test_arquivo_upload_lei_sistema(client, login, url, componente):
    """ Testa upload do arquivo relativo a lei do sistema pelo cadastrador """

    municipio = mommy.make("Municipio")
    plano = mommy.make("PlanoTrabalho")

    login.municipio = municipio
    login.plano_trabalho = plano
    login.save()

    arquivo = SimpleUploadedFile(
        "componente.txt", b"file_content", content_type="text/plain"
    )

    response = client.post(
        url, data={"arquivo": arquivo, "cnpj_fundo_cultura": "39791103000152"}
    )

    plano.refresh_from_db()
    sistema = getattr(plano, componente)

    assert response.status_code == 302
    assert sistema.arquivo.file.name.split("/")[-1] == arquivo.name

    plano.delete()
    municipio.delete()


def test_planotrabalho_view_reverte_com_namespace_e_name(client, plano_trabalho):
    """
    Verifica se a view PlanoTrabalho retorna como planotrabalho:detail
    """

    name = resolve(f"/planotrabalho/{plano_trabalho.id}/")
    assert name.url_name == "detail"


def test_planotrabalho_view_retorna_template_padrao(client, plano_trabalho):
    """
    Verifica se a class PlanoTrabalho utiliza o template padrão(planotrabalho_detail.html)
    """

    url = reverse("planotrabalho:detail", kwargs={"pk": plano_trabalho.id})
    response = client.get(url)

    assert "planotrabalho/planotrabalho_detail.html" in response.template_name


def test_cadastrarsistema_view_reverte_com_namespace(client):
    """
    Verifica se a view CadastrarSistema retorna como planotrabalho:cadastrarsistema
    """

    name = resolve(f"/planotrabalho/sistema/")

    assert name.url_name == "cadastrar_sistema"


def test_cadastrarsistema_view_retorna_template_padrao(client, login):
    """
    Verifica se a class CadastrarSistema utiliza o template
    padrão(cadastrarsistema_form.html)
    """

    url = reverse("planotrabalho:cadastrar_sistema")
    response = client.get(url)

    assert "planotrabalho/criacaosistema_form.html" in response.template_name


def test_cadastrarsistema_view_redireciona_para_planotrabalho(client, login):
    """
    Verifica se a view CadastrarSistema redireciona para a view PlanoTrabalho
    após uma operação bem sucedida.
    """

    url = reverse("planotrabalho:cadastrar_sistema")
    plano_trabalho = mommy.make('PlanoTrabalho')
    ente_federado = mommy.make('Municipio', _fill_optional=['cidade'])
    login.municipio = ente_federado
    login.plano_trabalho = plano_trabalho
    login.save()

    arquivo = SimpleUploadedFile(
        "componente.txt", b"file_content", content_type="text/plain"
    )

    data = {
        "arquivo": arquivo,
    }

    response = client.post(url, data)
    assert response.status_code == 302

    response_content = resolve(response.url)
    assert response_content.kwargs.get("pk") == str(plano_trabalho.pk)

    plano_trabalho.delete()
    ente_federado.delete()
