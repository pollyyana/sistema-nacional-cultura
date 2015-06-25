from django.shortcuts import render
from django.views.generic import ListView

from adesao.models import Usuario


# Create your views here.
def acompanhar_adesao(request):
    return render(request, 'adesao/acompanhar.html')


class AcompanharAdesao(ListView):
    queryset = Usuario.objects.filter(estado_processo='1')
    template_name = 'gestao/adesao/acompanhar.html'
    paginate_by = 2
