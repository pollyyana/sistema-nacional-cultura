from rest_framework import serializers
from adesao.models import Municipio, Cidade, Usuario
from planotrabalho.models import PlanoTrabalho, CriacaoSistema, OrgaoGestor,ConselhoCultural, FundoCultura, PlanoCultura
from django_filters.rest_framework import DjangoFilterBackend

# Componentes do Plano de Trabalho
class CriacaoSistemaSerializer(serializers.ModelSerializer):
    situacao_lei_sistema = serializers.ReadOnlyField(
            source = 'situacao_lei_sistema.descricao')
    class Meta:
        model = CriacaoSistema
        fields = ('lei_sistema_cultura', 'situacao_lei_sistema')

class OrgaoGestorSerializer(serializers.ModelSerializer):
    situacao_relatorio_secretaria = serializers.ReadOnlyField(
            source = 'situacao_relatorio_secretaria.descricao')
    class Meta:
        model = OrgaoGestor
        fields = ('relatorio_atividade_secretaria',
                  'situacao_relatorio_secretaria')

class ConselhoCulturalSerializer(serializers.ModelSerializer):
    situacao_ata = serializers.ReadOnlyField(
            source = 'situacao_ata.descricao')
    class Meta:
        model = ConselhoCultural
        fields = ('ata_regimento_aprovado','situacao_ata')

class FundoCulturaSerializer(serializers.ModelSerializer):
    situacao_lei_plano = serializers.ReadOnlyField(
            source = 'situacao_lei_plano.descricao')
    class Meta:
        model = FundoCultura
        fields = ('cnpj_fundo_cultura','lei_fundo_cultura',
                  'situacao_lei_plano')

class PlanoCulturaSerializer(serializers.ModelSerializer):
    situacao_lei_plano = serializers.ReadOnlyField(
            source = 'situacao_lei_plano.descricao')
    class Meta:
        model = PlanoCultura
        fields = ('relatorio_diretrizes_aprovadas', 'minuta_preparada',
                  'ata_reuniao_aprovacao_plano', 'ata_votacao_projeto_lei',
                  'lei_plano_cultura','situacao_lei_plano')

# Plano de Trabalho
class PlanoTrabalhoSerializer(serializers.ModelSerializer):
    criacao_sistema = CriacaoSistemaSerializer()
    orgao_gestor = OrgaoGestorSerializer()
    conselho_cultural = ConselhoCulturalSerializer()
    fundo_cultura = FundoCulturaSerializer()
    plano_cultura = PlanoCulturaSerializer()
    class Meta:
        model = PlanoTrabalho
        fields = ('id','criacao_sistema','orgao_gestor','conselho_cultural',
                  'fundo_cultura','plano_cultura')

# Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    plano_trabalho = PlanoTrabalhoSerializer()
    class Meta:
        model = Usuario
        fields = ('id','nome_usuario', 'municipio', 'responsavel',
                   'plano_trabalho', 'estado_processo','data_publicacao_acordo',
                   'codigo_ativacao','data_cadastro','prazo')

# Municipio
class MunicipioSerializer(serializers.ModelSerializer):
    cidade= serializers.ReadOnlyField(source='cidade.nome_municipio')
    estado = serializers.ReadOnlyField(source='estado.sigla')
    estado_expeditor = serializers.ReadOnlyField(source='estado_expeditor.sigla')
    usuario = UsuarioSerializer()
    class Meta:
        model = Municipio
        fields = ('id', 'cpf_prefeito', 'nome_prefeito', 'cnpj_prefeitura',
                   'rg_prefeito', 'termo_posse_prefeito','rg_copia_prefeito',
                   'cpf_copia_prefeito','email_institucional_prefeito',
                   'orgao_expeditor_rg','estado_expeditor', 'endereco', 
                   'complemento', 'cep','bairro','cidade','estado',
                   'endereco_eletronico','telefone_um','telefone_dois',
                   'telefone_tres','usuario')
