from django.shortcuts import redirect
from django.views.generic import ListView

from adesao.models import Usuario


# Create your views here.
def alterar_situacao(request, id):
    if request.method == "POST":
        for k, v in request.POST.items():
            print("Key: "+k+" Valor: "+v+"\n")
    return redirect('gestao:acompanhar_adesao')


class AcompanharAdesao(ListView):
    queryset = Usuario.objects.filter(estado_processo__range=('1', '6'))
    template_name = 'gestao/adesao/acompanhar.html'
    paginate_by = 10
