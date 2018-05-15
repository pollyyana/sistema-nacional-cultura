import pytest


@pytest.fixture(scope='session')
def situacoes(django_db_setup, django_db_blocker):
    """
    Cria situações dos arquivos do Plano Trabalho enviados no banco de testes
    """
    with django_db_blocker.unblock():


        from planotrabalho.models import SituacoesArquivoPlano

        situacoes = (
            (0, 'Em preenchimento'),
            (1, 'Avaliando anexo'),
            (2, 'Concluída'),
            (3, 'Arquivo aprovado com ressalvas'),
            (4, 'Arquivo danificado'),
            (5, 'Arquivo incompleto'),
            (6, 'Arquivo incorreto'),
        )

        for situacao in situacoes:
            SituacoesArquivoPlano.objects.create(id=situacao[0], descricao=situacao[1])

        return SituacoesArquivoPlano.objects.all()


