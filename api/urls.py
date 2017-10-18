from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views


urlpatterns = [
    url(r'^adesoes/$', views.MunicipioList.as_view()),
    url(r'^adesoes/(?P<pk>[0-9]+)/$', views.MunicipioDetail.as_view()),
    
    
    url(r'^usuarios/$', views.UsuarioList.as_view()),
    url(r'^usuarios/(?P<pk>[0-9]+)/$', views.UsuarioDetail.as_view()),
    
    url(r'^planostrabalho/$', views.PlanoTrabalhoList.as_view()),
    url(r'^planostrabalho/(?P<pk>[0-9]+)/$', views.PlanoTrabalhoDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
