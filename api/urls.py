from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    url(r'^adesoes/$', views.municipio_list),
    url(r'^adesoes/(?P<pk>[0-9]+)/$', views.municipio_detail),

    url(r'^usuarios/$', views.Usuarios_list.as_view())
    
]
urlpatterns = format_suffix_patterns(urlpatterns)
