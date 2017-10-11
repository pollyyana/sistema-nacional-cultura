from rest_framework import status 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response 

from planotrabalho.models import PlanoTrabalho
from adesao.models import Municipio, Cidade, Usuario
from api.serializers import MunicipioSerializer, UsuarioSerializer, PlanoTrabalhoSerializer

# MUNICIPIOS
@api_view(['GET'])
def municipio_list(request, format=None):
    if request.method == 'GET':
        municipios = Municipio.objects.filter().order_by('id')[:30]
        serializer = MunicipioSerializer(municipios, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def municipio_detail(request, pk, format=None):
    try:
        municipio = Municipio.objects.get(pk=pk)
    except Municipio.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MunicipioSerializer(municipio)
        return Response(serializer.data)


# PLANO TRABALHO
@api_view(['GET'])
def planoTrabalho_list(request, format=None):
    if request.method == 'GET':
        plano = PlanoTrabalho.objects.filter().order_by('id')[:30]
        serializer = PlanoTrabalhoSerializer(plano, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def planoTrabalho_detail(request, pk, format=None):
    try:
        plano = PlanoTrabalho.objects.get(pk=pk)
    except PlanoTrabalho.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlanoTrabalhoSerializer(plano)
        return Response(serializer.data)
    

# USUÁRIOS    
@api_view(['GET'])
def usuarios_detail(request, pk, format=None):
    try:
        usuarios = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = UsuarioSerializer(usuarios)
        return Response(serializer.data)
    
class Usuarios_list(APIView):
    def get(self, request, format=None):
            usuarios = Usuario.objects.filter().order_by('id')[:30]
            serializer = UsuarioSerializer(usuarios, many=True)
            return Response(serializer.data)
        
    
        