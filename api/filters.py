from django.db.models import Q

from django_filters import rest_framework as filters

from planotrabalho.models import PlanoTrabalho
from adesao.models import Municipio


class MunicipioFilter(filters.FilterSet):
    estado_sigla = filters.CharFilter(name='estado__sigla', lookup_expr='iexact')
    nome_uf = filters.CharFilter(name='estado__nome_uf', lookup_expr='iexact')
    nome_municipio = filters.CharFilter(name='cidade__nome_municipio', lookup_expr='iexact')
    situacao_adesao = filters.CharFilter(name='usuario__estado_processo',
                                         lookup_expr='istartswith')
    data_adesao = filters.DateFilter(name='usuario__data_publicacao_acordo')
    data_adesao_min = filters.DateFilter(name='usuario__data_publicacao_acordo', lookup_expr=('gte'))
    data_adesao_max = filters.DateFilter(name='usuario__data_publicacao_acordo', lookup_expr=('lte'))
    municipal = filters.BooleanFilter(method='municipal_filter')
    estadual = filters.BooleanFilter(method='estadual_filter')
    ente_federado = filters.CharFilter(method='ente_federado_filter')

    situacao_conselho_id = filters.NumberFilter(name='usuario__plano_trabalho__conselho_cultural__situacao__id')
    situacao_orgao_id = filters.NumberFilter(name='usuario__plano_trabalho__orgao_gestor__situacao__id')
    situacao_lei_id = filters.NumberFilter(name='usuario__plano_trabalho__criacao_sistema__situacao__id')
    situacao_fundo_id = filters.NumberFilter(name='usuario__plano_trabalho__fundo_cultura__situacao__id')
    situacao_plano_id = filters.NumberFilter(name='usuario__plano_trabalho__plano_cultura__situacao__id')

    situacao_conselho_descricao = filters.CharFilter(name='usuario__plano_trabalho__conselho_cultural__situacao__descricao',
                                                     lookup_expr='istartswith')
    situacao_orgao_descricao = filters.CharFilter(name='usuario__plano_trabalho__orgao_gestor__situacao__descricao',
                                                  lookup_expr='istartswith')
    situacao_lei_descricao = filters.CharFilter(name='usuario__plano_trabalho__criacao_sistema__situacao__descricao',
                                                lookup_expr='istartswith')
    situacao_fundo_descricao = filters.CharFilter(name='usuario__plano_trabalho__fundo_cultura__situacao__descricao',
                                                  lookup_expr='istartswith')
    situacao_plano_descricao = filters.CharFilter(name='usuario__plano_trabalho__plano_cultura__situacao__descricao',
                                                  lookup_expr='istartswith')

    def ente_federado_filter(self, queryset, name, value):

        return queryset.filter(
                Q(estado__sigla__istartswith=value) |
                Q(estado__nome_uf__istartswith=value) |
                Q(cidade__nome_municipio__istartswith=value))

    def estadual_filter(self, queryset, name, value):

        return queryset.filter(cidade__isnull=value)

    def municipal_filter(self, queryset, name, value):
        isnull = not value

        return queryset.filter(cidade__isnull=isnull)

    class Meta:
        model = Municipio
        fields = ('id', 'cnpj_prefeitura', 'data_adesao',
                  'data_adesao_min', 'data_adesao_max')


class PlanoTrabalhoFilter(filters.FilterSet):
    SITUACOES_IDS = (
        (0, 'Em preenchimento'),
        (1, 'Avaliando anexo'),
        (2, 'Concluída'),
        (3, 'Arquivo aprovado com ressalvas'),
        (4, 'Arquivo danificado'),
        (5, 'Arquivo incompleto'),
        (6, 'Arquivo incorreto'),
    )

    SITUACOES_DESCRICOES = (
        ('Em preenchimento', 'Em preenchimento'),
        ('Avaliando anexo', 'Avaliando anexo'),
        ('Concluída', 'Concluída'),
        ('Arquivo aprovado com ressalvas', 'Arquivo aprovado com ressalvas'),
        ('Arquivo danificado', 'Arquivo danificado'),
        ('Arquivo incompleto', 'Arquivo incompleto'),
        ('Arquivo incorreto', 'Arquivo incorreto'),
    )

    situacao_conselho_id = filters.MultipleChoiceFilter(choices=SITUACOES_IDS, name='conselho_cultural__situacao__id')
    situacao_conselho_descricao = filters.MultipleChoiceFilter(choices=SITUACOES_DESCRICOES, name='conselho_cultural__situacao__descricao',
                                                     lookup_expr='istartswith')

    situacao_orgao_id = filters.MultipleChoiceFilter(choices=SITUACOES_IDS, name='orgao_gestor__situacao__id')
    situacao_orgao_descricao = filters.MultipleChoiceFilter(choices=SITUACOES_DESCRICOES, name='orgao_gestor__situacao__descricao',
                                                  lookup_expr='istartswith')

    situacao_lei_id = filters.MultipleChoiceFilter(choices=SITUACOES_IDS, name='criacao_sistema__situacao__id')
    situacao_lei_descricao = filters.MultipleChoiceFilter(choices=SITUACOES_DESCRICOES, name='criacao_sistema__situacao__descricao',
                                                lookup_expr='istartswith')

    situacao_fundo_id = filters.MultipleChoiceFilter(choices=SITUACOES_IDS, name='fundo_cultura__situacao__id')
    situacao_fundo_descricao = filters.MultipleChoiceFilter(choices=SITUACOES_DESCRICOES, name='fundo_cultura__situacao__descricao',
                                                  lookup_expr='istartswith')

    situacao_plano_id = filters.MultipleChoiceFilter(choices=SITUACOES_IDS, name='plano_cultura__situacao__id')
    situacao_plano_descricao = filters.MultipleChoiceFilter(choices=SITUACOES_DESCRICOES, name='plano_cultura__situacao__descricao',
                                                  lookup_expr='istartswith')

    class Meta:
        model = PlanoTrabalho
        fields = ('id',)
