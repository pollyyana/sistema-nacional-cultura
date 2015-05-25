from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name='login'),
    url(r'^sair/$', 'django.contrib.auth.views.logout',
        {'template_name': 'index.html'}, name='logout'),
    url(r'^ativar/usuario/(?P<codigo>[\w]+)/$',
        views.ativar_usuario, name='ativar_usuario'),


    url(r'^home/', views.home, name='home'),
    url(r'^usuario/$', views.CadastrarUsuario.as_view(), name='usuario'),

    # Cadastro e alteração de prefeitura
    url(r'^municipio/$', login_required(views.CadastrarMunicipio.as_view()),
        name='municipio'),
    url(r'^municipio/(?P<pk>[0-9]+)/$',
        login_required(views.AlterarMunicipio.as_view()),
        name='alterar_municipio'),

    # Cadastro e alteração de responsável
    url(r'^responsavel/$', login_required(views.CadastrarResponsavel.as_view()),
        name='responsavel'),
    url(r'^responsavel/(?P<pk>[0-9]+)/$',
        login_required(views.AlterarResponsavel.as_view()),
        name='alterar_responsavel'),

    # Cadastro e alteração de secretário
    url(r'^secretario/$', login_required(views.CadastrarSecretario.as_view()),
        name='secretario'),
    url(r'^secretario/(?P<pk>[0-9]+)/$',
        login_required(views.AlterarSecretario.as_view()),
        name='alterar_secretario'),

    # Minuta de acordo e termo de solicitação
    url(r'^termo/minuta/$',
        login_required(views.MinutaAcordo.as_view()),
        name='minuta'),
    url(r'^termo/solicitacao/$',
        login_required(views.TermoSolicitacao.as_view()),
        name='solicitacao'),
]
