from rest_framework import serializers
from adesao.models import Municipio, Cidade, Usuario
from planotrabalho.models import PlanoTrabalho

class PlanoTrabalhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanoTrabalho
        fields = ('criacao_sistema','orgao_gestor','conselho_cultural',
                  'fundo_cultura','plano_cultura')

class UsuarioSerializer(serializers.ModelSerializer):
    plano_trabalho = PlanoTrabalhoSerializer()
    class Meta:
        model = Usuario
        fields = ('id','nome_usuario', 'municipio', 'responsavel',
                   'plano_trabalho', 'estado_processo','data_publicacao_acordo',
                   'codigo_ativacao','data_cadastro','prazo')

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
