from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from . import views

urlpatterns = [
    url(r'^$', staff_member_required(
        views.AcompanharAdesao.as_view(),
        login_url='adesao:login'), name='acompanhar_adesao'),
    url(r'alterar/situacao/(?P<id>[\w]+)$',
        views.alterar_situacao,
        name='alterar_situacao'),
]
