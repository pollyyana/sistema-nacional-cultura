from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

schema_view = get_swagger_view(title='Dados SNC')

urlpatterns = [
    url(r'^$', schema_view),

    url(r'^adesoes/$', views.MunicipioList.as_view()),
    url(r'^adesoes/(?P<pk>[0-9]+)/$', views.MunicipioDetail.as_view(), name='municipio-detail'),
    
    url(r'^usuarios/$', views.UsuarioList.as_view()),
    url(r'^usuarios/(?P<pk>[0-9]+)/$', views.UsuarioDetail.as_view(), name='usuario-detail'),
    
    url(r'^planostrabalho/$', views.PlanoTrabalhoList.as_view()),
    url(r'^planostrabalho/(?P<pk>[0-9]+)/$', views.PlanoTrabalhoDetail.as_view(), name='planotrabalho-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
