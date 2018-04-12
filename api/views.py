from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics

from adesao.models import Municipio
from planotrabalho.models import PlanoTrabalho
from api.serializers import MunicipioSerializer
from api.serializers import PlanoTrabalhoSerializer
from api.filters import MunicipioFilter
from api.filters import PlanoTrabalhoFilter


def swagger_index(request):
    return render(request, 'swagger/index.html')


class MunicipioList(generics.ListAPIView):
    queryset = Municipio.objects.filter().order_by('-id')
    serializer_class = MunicipioSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = MunicipioFilter


class MunicipioDetail(generics.RetrieveAPIView):
    queryset = Municipio.objects.filter().order_by('-id')
    serializer_class = MunicipioSerializer


class PlanoTrabalhoList(generics.ListAPIView):
    queryset = PlanoTrabalho.objects.filter().order_by('-id')
    serializer_class = PlanoTrabalhoSerializer

    filter_backends = (DjangoFilterBackend,)
    filter_class = PlanoTrabalhoFilter


class PlanoTrabalhoDetail(generics.RetrieveAPIView):
    queryset = PlanoTrabalho.objects.filter().order_by('-id')
    serializer_class = PlanoTrabalhoSerializer
