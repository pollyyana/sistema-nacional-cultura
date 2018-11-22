from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count

from rest_framework import filters
from rest_framework import generics
from rest_framework.response import Response

from adesao.models import SistemaCultura
from adesao.models import Municipio
from planotrabalho.models import PlanoTrabalho

from .serializers import MunicipioSerializer
from .serializers import MunicipioSerializer as SistemaCulturaSerializer
from .serializers import PlanoTrabalhoSerializer

from .filters import SistemaCulturaFilter
from .filters import MunicipioFilter
from .filters import PlanoTrabalhoFilter

from .metadata import MunicipioMetadata as SistemaCulturaMetadata
from .metadata import PlanoTrabalhoMetadata


def swagger_index(request):
    return render(request, 'swagger/index.html')


class SistemaCulturaAPIList(generics.ListAPIView):
    queryset = SistemaCultura.sistema.all()
    serializer_class = SistemaCulturaSerializer
    metadata_class = SistemaCulturaMetadata

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filterset_class = SistemaCulturaFilter
    ordering_fields = ('ente_federado__nome', 'estado__nome_uf')

    def get_extra_counts(self): 
        queryset = self.filter_queryset(self.get_queryset())
        
        return queryset.aggregate(
            municipios=Count('pk', filter=Q(cidade__isnull=False)),
            municipios_aderidos=Count('pk', filter=(Q(usuario__estado_processo=6) & Q(cidade__isnull=False))),
            estados=Count('pk', filter=Q(cidade__isnull=True)),
            estados_aderidos=Count('pk', filter=(Q(usuario__estado_processo=6) & Q(cidade__isnull=True))),
        )

    def list(self, request):
        response = super().list(self, request)
        extra_counts = self.get_extra_counts()
        response.data['municipios'] = extra_counts['municipios']
        response.data['municipios_aderidos'] = extra_counts['municipios_aderidos']
        response.data['estados'] = extra_counts['estados']
        response.data['estados_aderidos'] = extra_counts['estados_aderidos']
        return response


class MunicipioDetail(generics.RetrieveAPIView):
    queryset = Municipio.objects.filter().order_by('-id')
    serializer_class = MunicipioSerializer


class PlanoTrabalhoList(generics.ListAPIView):
    queryset = PlanoTrabalho.objects.filter().order_by('-id')
    serializer_class = PlanoTrabalhoSerializer
    metadata_class = PlanoTrabalhoMetadata

    filter_backends = (DjangoFilterBackend,)
    filterset_class = PlanoTrabalhoFilter


class PlanoTrabalhoDetail(generics.RetrieveAPIView):
    queryset = PlanoTrabalho.objects.filter().order_by('-id')
    serializer_class = PlanoTrabalhoSerializer
