import pytest

from model_mommy import mommy
from django.core.files.uploadedfile import SimpleUploadedFile

from planotrabalho.models import CriacaoSistema


def test_criacaosistema_model_cria_nova_instancia_ao_modificar(client):
    """
    Verifica se ao tentar modificar uma instancia de CriacaoSistema é 
    criado um novo registro.
    """

    sistema = mommy.make("CriacaoSistema")
    
    arquivo = SimpleUploadedFile(
        "componente.txt", b"file_content", content_type="text/plain"
    )

    sistema.arquivo = arquivo
    sistema.save()

    assert CriacaoSistema.objects.count() == 2
