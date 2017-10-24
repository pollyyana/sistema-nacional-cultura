from rest_framework import serializers
from drf_hal_json import serializers as hal_serializers
from adesao.models import Municipio, Uf, Cidade, Usuario
from planotrabalho.models import (PlanoTrabalho, CriacaoSistema, OrgaoGestor,
ConselhoCultural, FundoCultura, PlanoCultura)
from drf_hal_json.fields import HalHyperlinkedRelatedField, HalContributeToLinkField

# Componentes do Plano de Trabalho
class CriacaoSistemaSerializer(hal_serializers.HalModelSerializer):
    situacao_lei_sistema = serializers.ReadOnlyField(
            source = 'situacao_lei_sistema.descricao')
    class Meta:
        model = CriacaoSistema
        fields = ('lei_sistema_cultura', 'situacao_lei_sistema')

class OrgaoGestorSerializer(hal_serializers.HalModelSerializer):
    situacao_relatorio_secretaria = serializers.ReadOnlyField(
            source = 'situacao_relatorio_secretaria.descricao')
    class Meta:
        model = OrgaoGestor
        fields = ('relatorio_atividade_secretaria',
                  'situacao_relatorio_secretaria')

class ConselhoCulturalSerializer(hal_serializers.HalModelSerializer):
    situacao_ata = serializers.ReadOnlyField(
            source = 'situacao_ata.descricao')
    
    class Meta:
        model = ConselhoCultural
        fields = ('ata_regimento_aprovado','situacao_ata')

class FundoCulturaSerializer(hal_serializers.HalModelSerializer):
    situacao_lei_plano = serializers.ReadOnlyField(
            source = 'situacao_lei_plano.descricao')
    class Meta:
        model = FundoCultura
        fields = ('cnpj_fundo_cultura','lei_fundo_cultura',
                  'situacao_lei_plano')

class PlanoCulturaSerializer(hal_serializers.HalModelSerializer):
    situacao_lei_plano = serializers.ReadOnlyField(
            source = 'situacao_lei_plano.descricao')
    class Meta:
        model = PlanoCultura
        fields = ('relatorio_diretrizes_aprovadas', 'minuta_preparada',
                  'ata_reuniao_aprovacao_plano', 'ata_votacao_projeto_lei',
                  'lei_plano_cultura','situacao_lei_plano')

# Plano de Trabalho
class PlanoTrabalhoSerializer(hal_serializers.HalModelSerializer):
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
class UsuarioSerializer(hal_serializers.HalModelSerializer):
    #plano_trabalho = PlanoTrabalhoSerializer()
    #municipio = serializers.ReadOnlyField(source = 'municipio.cidade.nome_municipio')
    responsavel = serializers.ReadOnlyField(source = 'responsavel.nome_responsavel')
    class Meta:
        model = Usuario
        fields = ('responsavel','estado_processo',
                  'data_publicacao_acordo','municipio','plano_trabalho')
    
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
class MunicipioSerializer(hal_serializers.HalModelSerializer):
    ente_federado = serializers.SerializerMethodField() 
    governo = serializers.SerializerMethodField()
    plano_trabalho = HalContributeToLinkField(place_on='plano_trabalho') 
    class Meta:
        model = Municipio
        fields = ('self','ente_federado','governo','endereco_eletronico','usuario','plano_trabalho')

    def get_plano_trabalho(self,obj):
        serializer = PlanoTrabalhoSerializer(obj.usuario.plano_trabalho)
        return serializer.data
         
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

    def get_governo(self,obj):
        governo = Governo(nome_prefeito=obj.nome_prefeito,
                email_institucional_prefeito=obj.email_institucional_prefeito,
                termo_posse_prefeito=obj.termo_posse_prefeito)
        serializer = GovernoSerializer(governo)
        
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

class Governo(object):
    def __init__(self, nome_prefeito, email_institucional_prefeito,
            termo_posse_prefeito):
        self.nome_prefeito = nome_prefeito
        self.email_institucional_prefeito = email_institucional_prefeito
        self.termo_posse_prefeito = termo_posse_prefeito

class Componentes(object):
    def __init__(self, lei_sistema_cultura, relatorio_atividades_gestor, ata_conselho_cultural, 
                 lei_fundo_cultura, lei_plano_cultura):
        self.lei_sistema_cultura = lei_sistema_cultura
        self.relatorio_atividades_gestor = relatorio_atividades_gestor
        self.ata_conselho_cultural = ata_conselho_culturalr
        self.lei_fundo_cultura = lei_fundo_cultura
        self.lei_plano_cultura = lei_plano_cultura
        
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

class GovernoSerializer(serializers.Serializer):
    nome_prefeito = serializers.CharField()
    email_institucional_prefeito = serializers.CharField()
    termo_posse_prefeito = serializers.FileField()
    
class ComponentesSerializer(serializers.Serializer):
    lei_sistema_cultura = serializers.CharField()
    relatorio_atividades_gestor = serializers.CharField()
    ata_conselho_cultural = serializers.FileField()
    lei_fundo_cultura = serializers.FileField()
    lei_plano_cultura = serializers.FileField()

    
# Classes para estruturar os objetos de PLANO TRABALHO
class LeiSistemaCultura (object):
    def __init__(self, data_planejada, data_lancamento):
        self.data_planejada = data_planejada
        self.data_lancamento = data_lancamento

class RelatorioAtividadesGestor (object):
    def __init__(self, data_planejada, data_lancamento):
        self.data_planejada = data_planejada
        self.data_lancamento = data_lancamento
        
class AtaConselhoCultural (object):
    def __init__(self, data_planejada, data_lancamento):
        self.data_planejada = data_planejada
        self.data_lancamento = data_lancamento
        
class LeiFundoCultura (object):
    def __init__(self, data_planejada, data_lancamento):
        self.data_planejada = data_planejada
        self.data_lancamento = data_lancamento
        
class LeiPlanoCultura (object):
    def __init__(self, data_planejada, data_lancamento):
        self.data_planejada = data_planejada
        self.data_lancamento = data_lancamento
        
    
# SERIALIZERS das classes de estruturação de PLANO TRABALHO
class LeiSistemaCulturaSerializer(serializers.Serializer):
    data_planejada = serializers.CharField()
    data_lancamento = serializers.CharField()
    
class RelatorioAtividadesGestorSerializer(serializers.Serializer):
    data_planejada = serializers.CharField()
    data_lancamento = serializers.CharField()
    
class AtaConselhoCulturalSerializer(serializers.Serializer):
    data_planejada = serializers.CharField()
    data_lancamento = serializers.CharField()
    
class LeiFundoCulturaSerializer(serializers.Serializer):
    data_planejada = serializers.CharField()
    data_lancamento = serializers.CharField()
    
class LeiPlanoCulturaSerializer(serializers.Serializer):
    data_planejada = serializers.CharField()
    data_lancamento = serializers.CharField()
    
    

# Classes para estruturar os objetos de COMPONENTES
class CompLeiSistemaCultura (object):
    def __init__(self, lei_sistema_cultura):
        self.lei_sistema_cultura = lei_sistema_cultura
        self.situacao_lei_sistema = situacao_lei_sistema
        
class CompRelatorioAtividadesGestor (object):
    def __init__(self, relatorio_atividade_secretaria):
        self.relatorio_atividade_secretaria = relatorio_atividade_secretaria

class CompAtaConselhoCultural (object):
    def __init__(self, ata_regimento_aprovado,):
        self.ata_regimento_aprovado = ata_regimento_aprovado
                
class CompLeiFundoCultura (object):
    def __init__(self, lei_fundo_cultura, cnpj_fundo_cultura):
        self.lei_fundo_cultura = lei_fundo_cultura
        self.cnpj_fundo_cultura = cnpj_fundo_cultura
        
class CompLeiPlanoCultura (object):
    def __init__(self, relatorio_diretrizes_aprovadas, minuta_preparada, ata_reuniao_aprovacao_plano, 
                ata_votacao_projeto_lei, lei_plano_cultura):
        self.relatorio_diretrizes_aprovadas = relatorio_diretrizes_aprovadas
        self.minuta_preparada = minuta_preparada
        self.ata_reuniao_aprovacao_plano = ata_reuniao_aprovacao_plano
        self.ata_votacao_projeto_lei = ata_votacao_projeto_lei
        self.lei_plano_cultura = lei_plano_cultura
        
# SERIALIZERS das classes de estruturação de COMPONENTES    
class CompLeiSistemaCulturaS(serializers.Serializer):
    lei_sistema_cultura = serializers.FileField()
    
class CompRelatorioAtividadesGestor(serializers.Serializer):
     relatorio_atividade_secretaria = serializers.FileField()

class CompAtaConselhoCultural(serializers.Serializer):
    ata_regimento_aprovado = serializers.FileField()
    
class CompLeiFundoCultura(serializers.Serializer):
    lei_fundo_cultura = serializers.FileField()
    cnpj_fundo_cultura = serializers.CharField()
    
class CompLeiPlanoCultura(serializers.Serializer):
    relatorio_diretrizes_aprovadas = serializers.FileField()
    minuta_preparada = serializers.FileField()
    ata_reuniao_aprovacao_plano = serializers.FileField()
    ata_votacao_projeto_lei = serializers.FileField()
    lei_plano_cultura = serializers.FileField()
