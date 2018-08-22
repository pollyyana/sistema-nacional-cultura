from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count

from rest_framework import filters
from rest_framework import generics
from rest_framework.response import Response

from adesao.models import Municipio
from planotrabalho.models import PlanoTrabalho
from api.serializers import MunicipioSerializer
from api.serializers import PlanoTrabalhoSerializer
from api.filters import MunicipioFilter
from api.filters import PlanoTrabalhoFilter
from api.metadata import MunicipioMetadata
from api.metadata import PlanoTrabalhoMetadata


def swagger_index(request):
    return render(request, 'swagger/index.html')


class MunicipioList(generics.ListAPIView):
    queryset = Municipio.objects.filter().order_by('-id')
    extra_counts = queryset.aggregate(
        cidades=Count('pk', filter=Q(cidade__isnull=False)),
        estados=Count('pk', filter=Q(cidade__isnull=True)),
        estados_aderidos=Count('pk', filter=(Q(usuario__estado_processo=6) & Q(cidade__isnull=True))),
        municipios_aderidos=Count('pk', filter=(Q(usuario__estado_processo=6) & Q(cidade__isnull=False))),
    )
    serializer_class = MunicipioSerializer
    metadata_class = MunicipioMetadata

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_class = MunicipioFilter
    ordering_fields = ('cidade__nome_municipio', 'estado__nome_uf')

    def list(self, request):
        response = super(MunicipioList, self).list(self, request)
        response.data['cidades'] = self.extra_counts['cidades']
        response.data['estados'] = self.extra_counts['estados']
        response.data['estados_aderidos'] = self.extra_counts['estados_aderidos']
        response.data['municipios_aderidos'] = self.extra_counts['municipios_aderidos']
        return response


class MunicipioDetail(generics.RetrieveAPIView):
    queryset = Municipio.objects.filter().order_by('-id')
    serializer_class = MunicipioSerializer


class PlanoTrabalhoList(generics.ListAPIView):
    queryset = PlanoTrabalho.objects.filter().order_by('-id')
    serializer_class = PlanoTrabalhoSerializer
    metadata_class = PlanoTrabalhoMetadata

    filter_backends = (DjangoFilterBackend,)
    filter_class = PlanoTrabalhoFilter


class PlanoTrabalhoDetail(generics.RetrieveAPIView):
    queryset = PlanoTrabalho.objects.filter().order_by('-id')
    serializer_class = PlanoTrabalhoSerializer
