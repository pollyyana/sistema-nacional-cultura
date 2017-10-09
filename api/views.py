from rest_framework import status 
from rest_framework.decorators import api_view 
from rest_framework.response import Response 

from adesao.models import Municipio, Cidade, Usuario
from api.serializers import MunicipioSerializer, UsuarioSerializer

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


@api_view(['GET'])    
def usuarios_list(request, format=None):
    if request.method == 'GET':
        usuarios = Usuario.objects.filter().order_by('id')[:30]
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

