from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import permission_required

from adesao.models import Usuario

from .forms import AlterarSituacao


# Create your views here.
@permission_required('user.is_staff')
def alterar_situacao(request, id):
    if request.method == "POST":
        form = AlterarSituacao(
            request.POST,
            instance=Usuario.objects.get(id=id))
        if form.is_valid():
            form.save()
    return redirect('gestao:acompanhar_adesao')


class AcompanharAdesao(ListView):
    queryset = Usuario.objects.filter(estado_processo__range=('1', '5'))
    template_name = 'gestao/adesao/acompanhar.html'
    paginate_by = 10
