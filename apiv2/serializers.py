from rest_framework import serializers
from drf_hal_json.fields import HalHyperlinkedIdentityField
from drf_hal_json import serializers as hal_serializers

from adesao.models import Municipio
from adesao.models import Uf
from adesao.models import Cidade
from planotrabalho.models import CriacaoSistema
from planotrabalho.models import OrgaoGestor
from planotrabalho.models import ConselhoCultural
from planotrabalho.models import FundoCultura
from planotrabalho.models import PlanoCultura
from planotrabalho.models import Conselheiro

from adesao.models import SistemaCultura
from planotrabalho.models import Componente
from adesao.models import EnteFederado
from adesao.models import Sede
from adesao.models import Gestor


# Criacao do Sistema
class CriacaoSistemaSerializer(hal_serializers.HalModelSerializer):
    situacao = serializers.ReadOnlyField(source='situacao.descricao')

    class Meta:
        model = CriacaoSistema
        fields = ('lei_sistema_cultura', 'situacao')


class OrgaoGestorSerializer(hal_serializers.HalModelSerializer):
    situacao = serializers.ReadOnlyField(source='situacao.descricao')

    class Meta:
        model = OrgaoGestor
        fields = ('relatorio_atividade_secretaria',
                  'situacao')


class ConselhoCulturalSerializer(hal_serializers.HalModelSerializer):
    situacao = serializers.ReadOnlyField(source='situacao.descricao')

    class Meta:
        model = ConselhoCultural
        fields = ('ata_regimento_aprovado', 'situacao')


class ConselheiroSerializer(hal_serializers.HalModelSerializer):
    situacao = serializers.SerializerMethodField()

    class Meta:
        model = Conselheiro
        fields = ['nome', 'segmento', 'email', 'situacao',
                  'data_cadastro', 'data_situacao']

    def get_situacao(self, obj):
        return obj.get_situacao_display()


class FundoCulturaSerializer(hal_serializers.HalModelSerializer):
    situacao = serializers.ReadOnlyField(source='situacao.descricao')

    class Meta:
        model = FundoCultura
        fields = ('cnpj_fundo_cultura', 'lei_fundo_cultura',
                  'situacao')


class PlanoCulturaSerializer(hal_serializers.HalModelSerializer):
    situacao = serializers.ReadOnlyField(source='situacao.descricao')

    class Meta:
        model = PlanoCultura
        fields = ('relatorio_diretrizes_aprovadas', 'minuta_preparada',
                  'ata_reuniao_aprovacao_plano', 'ata_votacao_projeto_lei',
                  'lei_plano_cultura', 'situacao')


class ComponenteSCSerializer(hal_serializers.HalModelSerializer):
    situacao = serializers.CharField(source='get_situacao_display')
    cod_situacao = serializers.CharField(source='situacao')

    class Meta:
        model = Componente
        fields = ('cod_situacao', 'situacao', 'data_envio', 'arquivo')


class PlanoTrabalhoSCSerializer(hal_serializers.HalModelSerializer):
    criacao_lei_sistema = ComponenteSCSerializer(source='legislacao')
    criacao_orgao_gestor = ComponenteSCSerializer(source='orgao_gestor')
    criacao_plano_cultura = ComponenteSCSerializer(source='plano')
    criacao_fundo_cultura = ComponenteSCSerializer(source='fundo_cultura')
    criacao_conselho_cultural = ComponenteSCSerializer(source='conselho')
    # _embedded = serializers.SerializerMethodField(method_name='get_embedded')
    self = HalHyperlinkedIdentityField(view_name='api:planotrabalho-detail')

    class Meta:
        model = SistemaCultura
        fields = (
            'id',
            'self',
            'criacao_lei_sistema',
            'criacao_orgao_gestor',
            'criacao_plano_cultura',
            'criacao_fundo_cultura',
            'criacao_conselho_cultural')


class PlanoTrabalhoSerializer(PlanoTrabalhoSCSerializer):

    class Meta:
        model = SistemaCultura
        fields = (
            'id',
            'self',
            'criacao_lei_sistema',
            'criacao_orgao_gestor',
            'criacao_plano_cultura',
            'criacao_fundo_cultura',
            'criacao_conselho_cultural')


class SedeSerializer(hal_serializers.HalModelSerializer):
    telefones = serializers.SerializerMethodField(source='telefones')
    localizacao = serializers.SerializerMethodField(source='localizacao')

    class Meta:
        model = Sede
        fields = ("localizacao", "telefones", "endereco_eletronico")

    def get_telefones(self, obj):
        return {
            "telefone_um": obj.telefone_um,
            "telefone_dois": obj.telefone_dois,
            "telefone_tres": obj.telefone_tres
        }

    def get_localizacao(self, obj):

        return {
            "cnpj": obj.cnpj,
            "endereco": obj.endereco,
            "cep": obj.cep,
            "bairro": obj.bairro,
            "complemento": obj.complemento
            }


class EnteFederadoSerializer(hal_serializers.HalModelSerializer):

    class Meta:
        model = EnteFederado
        fields = (
            "cod_ibge",
            "nome",
            "territorio",
            "populacao",
            "idh",
            "is_municipio",
            "sigla")


class GestorSerializer(hal_serializers.HalModelSerializer):
    termo_posse_prefeito = serializers.CharField(source='termo_posse')
    nome_prefeito = serializers.CharField(source='nome')

    class Meta:
        model = Gestor
        fields = ("email_institucional", "nome_prefeito", "termo_posse_prefeito")


class SistemaCulturaSerializer(hal_serializers.HalModelSerializer):
    self = HalHyperlinkedIdentityField(view_name='api:sistemacultura-detail')
    acoes_plano_trabalho = serializers.SerializerMethodField()
    ente_federado = EnteFederadoSerializer()
    governo = GestorSerializer(source='gestor')
    situacao_adesao = serializers.CharField(source='get_estado_processo_display')
    cod_situacao_adesao = serializers.CharField(source='estado_processo')
    data_adesao = serializers.DateField(source='data_publicacao_acordo')
    conselho = serializers.SerializerMethodField()
    sede = SedeSerializer()

    class Meta:
        model = SistemaCultura
        fields = (
            "id",
            "self",
            "data_adesao",
            "situacao_adesao",
            "cod_situacao_adesao",
            "acoes_plano_trabalho",
            "ente_federado",
            "governo",
            "conselho",
            "sede")

    def get_conselho(self, obj):
        return ("")
        # print(obj.conselho)
        # return ("asdasd")
        # try:
        #     conselho = obj.conselho
        #     assert conselho
        # except (Usuario.DoesNotExist, AssertionError):
        #     return None

        # context = {}
        # context['request'] = self.context['request']
        # serializer = ConselheiroSerializer(instance=conselho, context=context)

        # return serializer.data

    def get_acoes_plano_trabalho(self, obj):
        planotrabalho = PlanoTrabalhoSCSerializer(instance=obj, context=self.context)
        return planotrabalho.data


class SistemaCulturaDetailSerializer(PlanoTrabalhoSCSerializer):
    self = HalHyperlinkedIdentityField(view_name='api:planotrabalho-detail')
    sistema_cultura_local = \
        HalHyperlinkedIdentityField(view_name='api:sistemacultura-detail')

    class Meta:
        model = SistemaCultura
        fields = (
            "self",
            "id",
            "criacao_lei_sistema",
            "criacao_orgao_gestor",
            "criacao_conselho_cultural",
            "criacao_fundo_cultura",
            "criacao_plano_cultura",
            "sistema_cultura_local"
            )

    def to_representation(self, instance):
        context = super(SistemaCulturaDetailSerializer, self).\
            to_representation(instance)
        embedded = context.pop('_embedded')

        responseContext = context.copy()
        responseContext.update(embedded)
 
        return responseContext