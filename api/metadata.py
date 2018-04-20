from rest_framework.metadata import SimpleMetadata

from adesao.models import LISTA_ESTADOS_PROCESSO
from planotrabalho.models import SituacoesArquivoPlano


class MunicipioMetadata(SimpleMetadata):

    def get_situacao_adesao(self):
        situacao_adesao = []

        for situacao in LISTA_ESTADOS_PROCESSO:
            data = {'id': situacao[0], 'description': situacao[1]}
            situacao_adesao.append(data)

        choices = {'choices': situacao_adesao}

        return choices

    def determine_metadata(self, request, view):
        metadata = super(MunicipioMetadata, self).determine_metadata(request, view)
        metadata['name'] = 'Sistema de Cultura Local'
        metadata['ente_federado'] = {}
        metadata['ente_federado']['situacao_adesao'] = self.get_situacao_adesao()

        return metadata


class PlanoTrabalhoMetadata(SimpleMetadata):
    def get_situacao_arquivos(self):
        situacoes = SituacoesArquivoPlano.objects.all()
        situacao_adesao = []

        for situacao in situacoes:
            data = {'id': situacao.id, 'description': situacao.descricao}
            situacao_adesao.append(data)

        choices = {'choices': situacao_adesao}

        return choices

    def determine_metadata(self, request, view):
        metadata = super(PlanoTrabalhoMetadata, self).determine_metadata(request, view)
        metadata['name'] = 'Ações do Plano de trabalho'
        metadata['situacao'] = self.get_situacao_arquivos()

        return metadata


