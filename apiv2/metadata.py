from rest_framework.metadata import SimpleMetadata

from adesao.models import LISTA_ESTADOS_PROCESSO
from planotrabalho.models import SituacoesArquivoPlano
from planotrabalho.forms import SETORIAIS
from planotrabalho.models import SITUACAO_CONSELHEIRO


class MunicipioMetadata(SimpleMetadata):

    def get_situacao_adesao(self):
        situacao_adesao = []

        for situacao in LISTA_ESTADOS_PROCESSO:
            data = {'id': situacao[0], 'description': situacao[1]}
            situacao_adesao.append(data)

        choices = {'choices': situacao_adesao}

        return choices

    def get_segmento_conselheiros(self):
        segmentos = []

        for segmento in SETORIAIS:
            data = {'id': segmento[0], 'description': segmento[1]}
            segmentos.append(data)

        choices = {'choices': segmentos}

        return choices

    def get_situacao_conselheiro(self):
        situacao_conselheiro = []

        for situacao in SITUACAO_CONSELHEIRO:
            data = {'id': situacao[0], 'description': situacao[1]}
            situacao_conselheiro.append(data)

        choices = {'choices': situacao_conselheiro}

        return choices

    def determine_metadata(self, request, view):
        metadata = super(MunicipioMetadata, self).determine_metadata(request, view)
        metadata['name'] = 'Sistema de Cultura Local'
        metadata['ente_federado'] = {}
        metadata['conselho'] = {}

        metadata['ente_federado']['situacao_adesao'] = self.get_situacao_adesao()
        metadata['conselho']['segmento'] = self.get_segmento_conselheiros()
        metadata['conselho']['situacao'] = self.get_situacao_conselheiro()

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
