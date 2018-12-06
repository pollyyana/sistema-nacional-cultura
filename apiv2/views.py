from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count

from rest_framework import filters
from rest_framework import generics
from rest_framework.response import Response

from adesao.models import SistemaCultura
from adesao.models import Municipio
from adesao.models import EnteFederado
from planotrabalho.models import PlanoTrabalho

from .serializers import MunicipioSerializer
# from .serializers import MunicipioSerializer as SistemaCulturaSerializer
from .serializers import SistemaCulturaSerializer
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
    ordering_fields = ('ente_federado__nome',)

    # def get_extra_counts(self): 
    #     queryset = self.filter_queryset(self.get_queryset())
        
    #     return queryset.aggregate(
    #         municipios=Count('pk', filter=Q(ente_federado__cod_ibge__gt=100)),
    #         municipios_aderidos=Count('pk', filter=(Q(estado_processo=6) & Q(ente_federado__cod_ibge__gt=100))),
    #         estados=Count('pk', filter=Q(ente_federado__cod_ibge__lte=100)),
    #         estados_aderidos=Count('pk', filter=(Q(estado_processo=6) & Q(ente_federado__cod_ibge__lte=100))),
    #     )

    def list(self, request):
        response = super().list(self, request)
        response.data['municipios'] = EnteFederado.objects.filter(cod_ibge__gt=100).count()
        response.data['municipios_aderidos'] = SistemaCultura.sistema.filter(estado_processo=6).filter(ente_federado__cod_ibge__gt=100).count()
        response.data['estados'] = EnteFederado.objects.filter(cod_ibge__lte=100).count()
        response.data['estados_aderidos'] = SistemaCultura.sistema.filter(ente_federado__cod_ibge__lte=100).filter(estado_processo=6).count()
        return response


class SistemaCulturaDetail(generics.RetrieveAPIView):
    queryset = SistemaCultura.objects.filter()
    serializer_class = SistemaCulturaSerializer



class PlanoTrabalhoList(generics.ListAPIView):
    queryset = PlanoTrabalho.objects.filter().order_by('-id')
    serializer_class = PlanoTrabalhoSerializer
    metadata_class = PlanoTrabalhoMetadata

    filter_backends = (DjangoFilterBackend,)
    filterset_class = PlanoTrabalhoFilter


class PlanoTrabalhoDetail(generics.RetrieveAPIView):
    queryset = PlanoTrabalho.objects.filter().order_by('-id')
    serializer_class = PlanoTrabalhoSerializer
