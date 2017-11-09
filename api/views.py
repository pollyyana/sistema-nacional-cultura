from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from planotrabalho.models import PlanoTrabalho 
from adesao.models import Municipio, Cidade, Usuario
from api.serializers import MunicipioSerializer, UsuarioSerializer, PlanoTrabalhoSerializer


# MUNICIPIOS
# Lista todos os municipios
class  MunicipioList(generics.ListAPIView):
    queryset = Municipio.objects.filter().order_by('-id')
    serializer_class = MunicipioSerializer
    
    def get_queryset(self):
        queryset = Municipio.objects.filter().order_by('-id')

        # Parâmetros de busca passados na requisição 
        cnpj_prefeitura = self.request.query_params.get('cnpj_prefeitura',None)
        sigla_estado = self.request.query_params.get('sigla_estado',None)
        nome_municipio = self.request.query_params.get('nome_municipio',None)

        search_params = {'cnpj_prefeitura': cnpj_prefeitura, 'estado__sigla': sigla_estado,
                         'cidade__nome_municipio': nome_municipio}

        # Lista parâmetros não vazios
        arguments = {}
        for key, value in search_params.items():
            if value:
                arguments[key] = value

        queryset = Municipio.objects.filter(**arguments)

        return queryset

# Retorna um municipio especificado pela pk
class MunicipioDetail(generics.RetrieveAPIView):
    queryset = Municipio.objects.filter().order_by('-id')
    serializer_class = MunicipioSerializer

# PLANO TRABALHO
# Lista todos os planos de trabalho 
class PlanoTrabalhoList(generics.ListAPIView):
    queryset = PlanoTrabalho.objects.filter().order_by('-id')
    serializer_class = PlanoTrabalhoSerializer 
    

# Retorna um plano de trabalho especificado pela pk
class PlanoTrabalhoDetail(generics.RetrieveAPIView):
    queryset = PlanoTrabalho.objects.filter().order_by('-id') 
    serializer_class = PlanoTrabalhoSerializer 

# USUÁRIOS
# Lista todos os usuários
class UsuarioList(generics.ListAPIView):
    queryset = Usuario.objects.filter().order_by('-id')
    serializer_class = UsuarioSerializer
    
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('nome_usuario','municipio')

# Retorna um usuário especificado pela pk
class UsuarioDetail(generics.RetrieveAPIView):
    queryset = Usuario.objects.filter().order_by('-id') 
    serializer_class = UsuarioSerializer

