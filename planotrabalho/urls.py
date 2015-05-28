from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$',
        login_required(views.PlanoTrabalho.as_view()),
        name='planotrabalho'),

    # Primeira etapa - Criação do Sistema de Cultura
    url(r'^sistema/$',
        login_required(views.CadastrarSistema.as_view()),
        name='sistema'),
    url(r'^sistema/(?P<pk>[0-9]+)/$',
        login_required(views.AlterarSistema.as_view()),
        name='alterar_sistema'),

    # Segunda etapa - Estruturação do Orgão Gestor
    url(r'^gestor/$',
        login_required(views.CadastrarOrgaoGestor.as_view()),
        name='gestor'),
    url(r'^gestor/(?P<pk>[0-9]+)/$',
        login_required(views.AlterarOrgaoGestor.as_view()),
        name='alterar_gestor'),

    # Terceira etapa - Criação do Conselho de Política Cultural
    url(r'^conselho/$',
        login_required(views.CadastrarConselho.as_view()),
        name='conselho'),
    url(r'^conselho/(?P<pk>[0-9]+)/$',
        login_required(views.AlterarConselho.as_view()),
        name='alterar_conselho'),

    # Quarta etapa - Criação do Fundo de Cultura
    url(r'^fundo/$',
        login_required(views.CadastrarFundo.as_view()),
        name='fundo'),
    url(r'^fundo/(?P<pk>[0-9]+)/$',
        login_required(views.AlterarFundo.as_view()),
        name='alterar_fundo'),

    # Quinta etapa - Elaboração do Plano de Cultura
    url(r'^plano/$',
        login_required(views.CadastrarPlano.as_view()),
        name='plano'),
    url(r'^plano/(?P<pk>[0-9]+)/$',
        login_required(views.AlterarPlano.as_view()),
        name='alterar_plano'),
]
