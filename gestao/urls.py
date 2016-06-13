from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from . import views

urlpatterns = [
    # Acompanhar andamento dos processos de adesão
    url(r'^$', staff_member_required(
        views.AcompanharAdesao.as_view(),
        login_url='adesao:login'), name='acompanhar_adesao'),
    url(r'^alterar/situacao/(?P<id>[\w]+)$',
        staff_member_required(views.alterar_situacao, login_url='adesao:login'),
        name='alterar_situacao'),
    url(r'^alterar/cadastrador/municipio/',
        staff_member_required(views.AlterarCadastrador.as_view()), name='alterar_cadastrador'),
    url(r'^alterar/cadastrador/estado/',
        staff_member_required(views.AlterarCadastradorEstado.as_view()), name='alterar_cadastrador_estado'),
    # Acompanhar e aditivar prazos dos municípios
    url(r'^acompanhar/prazo/',
        staff_member_required(views.AcompanharPrazo.as_view()), name='acompanhar_prazo'),
    url(r'^aditivar/prazo/(?P<id>[\w]+)$',
        staff_member_required(views.aditivar_prazo, login_url='adesao:login'), name='aditivar_prazo'),

    # Acompanhar criação do sistema de cultura
    url(r'^acompanhar/sistema$', staff_member_required(
        views.AcompanharSistema.as_view(),
        login_url='adesao:login'), name='acompanhar_sistema'),
    # Acompanhar criação do órgão gestor
    url(r'^acompanhar/orgao$', staff_member_required(
        views.AcompanharOrgao.as_view(),
        login_url='adesao:login'), name='acompanhar_orgao'),
    # Acompanhar criação do conselho cultural
    url(r'^acompanhar/conselho$', staff_member_required(
        views.AcompanharConselho.as_view(),
        login_url='adesao:login'), name='acompanhar_conselho'),
    # Acompanhar criação do fundo de cultura
    url(r'^acompanhar/fundo$', staff_member_required(
        views.AcompanharFundo.as_view(),
        login_url='adesao:login'), name='acompanhar_fundo'),
    # Acompanhar elaboração do plano de cultura
    url(r'^acompanhar/plano$', staff_member_required(
        views.AcompanharPlano.as_view(),
        login_url='adesao:login'), name='acompanhar_plano'),

    # Diligência no anexo
    url(r'^diligencia/(?P<etapa>[\w]+)/(?P<st>[\w]+)/(?P<id>[\w]+)$',
        staff_member_required(
            views.diligencia_documental,
            login_url='adesao:login'), name='diligencia_documental'),
    # Conclusão da etapa
    url(r'^concluir/(?P<etapa>[\w]+)/(?P<st>[\w]+)/(?P<id>[\w]+)$',
        staff_member_required(
            views.concluir_etapa,
            login_url='adesao:login'), name='concluir_etapa'),

    # Detalhar usuário
    url(r'^detalhar/municipio/(?P<pk>[0-9]+)$',
        views.DetalharUsuario.as_view(),
        name='detalhar'),
    url(r'^usuarios/',
        staff_member_required(
            views.ListarUsuarios.as_view(),
            login_url='adesao:login'), name='usuarios'),
    url(r'^alterar/usuario/(?P<id>[\w]+)$',
        staff_member_required(
            views.AlterarUsuario.as_view(),
            login_url='adesao:login'), name='alterar_usuario'),

    # UF e Município aninhados
    url(r'^chain/municipio$', staff_member_required(views.MunicipioChain.as_view()), name='municipio_chain'),
]
