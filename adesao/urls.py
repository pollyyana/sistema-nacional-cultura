from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}, name='login'),
    url(r'^sair/$', 'django.contrib.auth.views.logout',
        {'template_name': 'index.html'}, name='logout'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset'),
    url(r'^home/', views.home, name='home'),
    url(r'^usuario/$', views.CadastrarUsuario.as_view(), name='usuario'),

    # Cadastro e alteração de prefeitura
    url(r'^municipio/$', login_required(views.CadastrarMunicipio.as_view()),
        name='municipio'),
    url(r'^prefeitura/(?P<municipio_id>[0-9]+)/$',
        login_required(views.AlterarMunicipio.as_view()),
        name='alterar_municipio'),

    # Cadastro e alteração de responsável
    url(r'^responsavel/$', login_required(views.CadastrarResponsavel.as_view()),
        name='responsavel'),
    url(r'^responsavel/(?P<responsavel_id>[0-9]+)/$',
        login_required(views.AlterarResponsavel.as_view()),
        name='alterar_responsavel'),

    # Cadastro e alteração de secretário
    url(r'^secretario/$', login_required(views.CadastrarSecretario.as_view()),
        name='secretario'),
    url(r'^secretario/(?P<secretario_id>[0-9]+)/$',
        login_required(views.AlterarSecretario.as_view()),
        name='alterar_secretario'),
]
