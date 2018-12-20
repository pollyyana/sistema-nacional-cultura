from django.db.models import Q

from django_filters import rest_framework as filters

from adesao.models import SistemaCultura, UFS
from planotrabalho.models import Componente


class SistemaCulturaFilter(filters.FilterSet):
    ente_federado = filters.\
        CharFilter(field_name='ente_federado__nome__unaccent', lookup_expr='icontains')
    estado_sigla = filters.CharFilter(method='sigla_filter')
    cnpj_prefeitura = filters.CharFilter(field_name='sede__cnpj', lookup_expr='contains')
    situacao_adesao = filters.\
        CharFilter(field_name='estado_processo', lookup_expr='exact')
    data_adesao = filters.DateFilter(field_name='data_publicacao_acordo')
    data_adesao_min = filters.\
        DateFilter(field_name='data_publicacao_acordo', lookup_expr=('gte'))
    data_adesao_max = filters.\
        DateFilter(field_name='data_publicacao_acordo', lookup_expr=('lte'))
    situacao_lei_sistema = filters.ModelMultipleChoiceFilter(
        queryset=Componente.objects.all(),
        field_name='legislacao__situacao',
        to_field_name='situacao'
    )
    situacao_orgao_gestor = filters.ModelMultipleChoiceFilter(
        queryset=Componente.objects.all(),
        field_name='orgao_gestor__situacao',
        to_field_name='situacao'
    )
    situacao_conselho_cultural = filters.ModelMultipleChoiceFilter(
        queryset=Componente.objects.all(),
        field_name='conselho__situacao',
        to_field_name='situacao'
    )
    situacao_fundo_cultura = filters.ModelMultipleChoiceFilter(
        queryset=Componente.objects.all(),
        field_name='fundo_cultura__situacao',
        to_field_name='situacao'
    )
    situacao_plano_cultura = filters.ModelMultipleChoiceFilter(
        queryset=Componente.objects.all(),
        field_name='plano__situacao',
        to_field_name='situacao'
    )
    municipal = filters.BooleanFilter(method='municipal_filter')
    estadual = filters.BooleanFilter(method='estadual_filter')

    class Meta:
        model = SistemaCultura
        fields = "__all__"

    def sigla_filter(self, queryset, name, value):
        try:
            inverseUf = {value: key for key, value in UFS.items()}
            cod_ibge = inverseUf[value.upper()]
        except Exception:
            cod_ibge = value

        return queryset.filter(Q(ente_federado__cod_ibge__startswith=cod_ibge))

    def estadual_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(ente_federado__cod_ibge__lte=100)

        return queryset

    def municipal_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(ente_federado__cod_ibge__gt=100)

        return queryset


class PlanoTrabalhoFilter(SistemaCulturaFilter):
    class Meta:
        model = SistemaCultura
        fields = "__all__"
