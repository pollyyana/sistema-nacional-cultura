from django.shortcuts import redirect
from django.views.generic import ListView

from adesao.models import Usuario

from .forms import AlterarSituacao


# Create your views here.
def alterar_situacao(request, id):
    if request.method == "POST":
        form = AlterarSituacao(
            request.POST,
            instance=Usuario.objects.get(id=id))
        if form.is_valid():
            form.save()
    return redirect('gestao:acompanhar_adesao')


class AcompanharAdesao(ListView):
    template_name = 'gestao/adesao/acompanhar.html'
    paginate_by = 10

    def get_queryset(self):
        situacao = self.request.GET.get('situacao', None)
        ente_federado = self.request.GET.get('municipio', None)

        if situacao and situacao in ('1', '2', '3', '4', '5'):
            return Usuario.objects.filter(estado_processo=situacao)

        if ente_federado:
            municipio = Usuario.objects.filter(
                municipio__cidade__nome_municipio=ente_federado)
            estado = Usuario.objects.filter(
                municipio__estado__sigla=ente_federado)

            return municipio if municipio else estado

        return Usuario.objects.filter(estado_processo__range=('1', '5'))
