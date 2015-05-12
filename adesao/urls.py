from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^home/', views.home, name='home'),
    url(r'^usuario/$', views.CadastrarUsuario.as_view(), name='usuario'),

    # Cadastro e alteração de prefeitura
    url(r'^municipio/$', views.CadastrarMunicipio.as_view(),
        name='municipio'),
    url(r'^prefeitura/(?P<municipio_id>[0-9]+)/$',
        views.alterar_prefeitura, name='alterar_municipio'),

    # Cadastro e alteração de responsável
    url(r'^responsavel/$', views.CadastrarResponsavel.as_view(),
        name='responsavel'),
    url(r'^responsavel/(?P<responsavel_id>[0-9]+)/$',
        views.alterar_responsavel, name='alterar_responsavel'),

    # Cadastro e alteração de secretário
    url(r'^secretario/$', views.CadastrarSecretario.as_view(),
        name='secretario'),
    url(r'^secretario/(?P<secretario_id>[0-9]+)/$',
        views.alterar_secretario, name='alterar_secretario'),
]
