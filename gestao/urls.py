from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.AcompanharAdesao.as_view(), name='acompanhar_adesao'),
    url(r'alterar/situacao/(?P<id>[\w]+)$',
        views.alterar_situacao,
        name='alterar_situacao'),
]
