from rest_framework import serializers
from adesao.models import Municipio, Uf, Cidade, Usuario
from planotrabalho.models import PlanoTrabalho, CriacaoSistema, OrgaoGestor,ConselhoCultural, FundoCultura, PlanoCultura

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
        fields = ('criacao_sistema','orgao_gestor','conselho_cultural',
                  'fundo_cultura','plano_cultura')

# Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    plano_trabalho = PlanoTrabalhoSerializer()
    municipio = serializers.ReadOnlyField(source = 'municipio.cidade.nome_municipio')
    responsavel = serializers.ReadOnlyField(source = 'responsavel.nome_responsavel')
    class Meta:
        model = Usuario
        fields = ('municipio', 'responsavel','plano_trabalho','estado_processo',
                  'data_publicacao_acordo')
# Cidade        
class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = ('codigo_ibge', 'nome_municipio')
# UF
class UfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uf 
        fields = ('codigo_ibge', 'sigla')

# Municipio
class MunicipioSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    ente_federado = serializers.SerializerMethodField() 

    class Meta:
        model = Municipio
        fields = ('ente_federado','nome_prefeito',
                  'termo_posse_prefeito', 'email_institucional_prefeito',
                  'endereco_eletronico','usuario')
 
    # Estrutura dados no objeto ente_federado
    def get_ente_federado(self,obj):
        localizacao = Localizacao(estado=obj.estado, cidade=obj.cidade,
                cep=obj.cep, bairro=obj.bairro, endereco=obj.endereco, complemento=obj.complemento)
        telefones = Telefones(telefone_um=obj.telefone_um, telefone_dois=obj.telefone_dois,
                telefone_tres=obj.telefone_tres) 
        ente_federado = EnteFederado(cnpj_prefeitura=obj.cnpj_prefeitura,localizacao=localizacao,
                telefones=telefones)
        serializer = EnteFederadoSerializer(ente_federado)

        return serializer.data 

# Classes para estruturar os objetos de adesoes
class EnteFederado(object):
    def __init__(self, cnpj_prefeitura, localizacao, telefones):
        self.cnpj_prefeitura = cnpj_prefeitura
        self.localizacao = localizacao
        self.telefones = telefones
 
class Localizacao(object):
    def __init__(self, estado, cidade, cep, bairro, endereco, complemento):
        self.estado = estado
        self.cidade = cidade 
        self.cep = cep 
        self.bairro = bairro
        self.endereco = endereco
        self.complemento = complemento

class Telefones(object):
    def __init__(self, telefone_um, telefone_dois, telefone_tres):
        self.telefone_um = telefone_um
        self.telefone_dois = telefone_dois
        self.telefone_tres = telefone_tres

# Serializers das classes de estruturação de adesoes
class LocalizacaoSerializer(serializers.Serializer):
    estado = UfSerializer() 
    cidade = CidadeSerializer()
    cep = serializers.CharField() 
    bairro = serializers.CharField() 
    endereco = serializers.CharField() 
    complemento = serializers.CharField() 

class TelefonesSerializer(serializers.Serializer):
    telefone_um = serializers.CharField()
    telefone_dois = serializers.CharField()
    telefone_tres = serializers.CharField()

class EnteFederadoSerializer(serializers.Serializer):
    cnpj_prefeitura = serializers.CharField()
    localizacao = LocalizacaoSerializer()
    telefones = TelefonesSerializer()

