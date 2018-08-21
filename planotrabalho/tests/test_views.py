import pytest

from django.shortcuts import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from model_mommy import mommy


@pytest.mark.parametrize(
    "url, componente",
    [
        (reverse("planotrabalho:sistema"), "criacao_sistema"),
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


def test_planotrabalho_view_retorna_template_padrao(client, plano_trabalho):
    """
    Verifica se a class PlanoTrabalho utiliza o template
    padrão(plano_trabalho_detail.html)
    """

    url = reverse("planotrabalho:planotrabalho", kwargs={'pk': plano_trabalho.id})
    response = client.get(url)

    assert response.template_name[0] == "planotrabalho/planotrabalho_detail.html"
