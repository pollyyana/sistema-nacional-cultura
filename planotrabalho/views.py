import json

from django.core import serializers
from django.shortcuts import redirect
from django.http import Http404, HttpResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy

from planotrabalho.models import PlanoTrabalho, CriacaoSistema, OrgaoGestor, Conselheiro
from planotrabalho.models import ConselhoCultural, FundoCultura, PlanoCultura
from .forms import CriarSistemaForm, OrgaoGestorForm, ConselhoCulturalForm
from .forms import FundoCulturaForm, PlanoCulturaForm


# Create your views here.
class PlanoTrabalho(DetailView):
    model = PlanoTrabalho
    template_name = 'planotrabalho/plano_trabalho.html'

    def get_context_data(self, **kwargs):
        plano = self.request.user.usuario.plano_trabalho
        context = super(PlanoTrabalho, self).get_context_data(**kwargs)
        datas_list = [
            plano.criacao_sistema,
            plano.orgao_gestor,
            plano.conselho_cultural,
            plano.fundo_cultura,
            plano.plano_cultura]
        context['datas_preenchidas'] = all(datas_list)
        return context

    def dispatch(self, *args, **kwargs):
        plano = self.request.user.usuario.plano_trabalho.id
        if str(plano) != self.kwargs['pk']:
            raise Http404()

        return super(PlanoTrabalho, self).dispatch(*args, **kwargs)


class CadastrarSistema(CreateView):
    form_class = CriarSistemaForm
    template_name = 'planotrabalho/cadastrar_sistema.html'

    def get_form_kwargs(self):
        kwargs = super(CadastrarSistema, self).get_form_kwargs()
        kwargs['user'] = self.request.user.usuario
        return kwargs

    def form_valid(self, form):
        self.request.user.usuario.plano_trabalho.criacao_sistema = form.save()
        self.request.user.usuario.plano_trabalho.save()
        return super(CadastrarSistema, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        sistema = self.request.user.usuario.plano_trabalho.criacao_sistema
        if sistema:
            return redirect('planotrabalho:alterar_sistema', pk=sistema.id)

        return super(CadastrarSistema, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        trabalho = self.request.user.usuario.plano_trabalho.id
        return reverse_lazy('planotrabalho:planotrabalho', args=[trabalho])


class AlterarSistema(UpdateView):
    form_class = CriarSistemaForm
    model = CriacaoSistema
    template_name = 'planotrabalho/cadastrar_sistema.html'

    def get_form_kwargs(self):
        kwargs = super(AlterarSistema, self).get_form_kwargs()
        kwargs['user'] = self.request.user.usuario
        return kwargs

    def get_success_url(self):
        trabalho = self.request.user.usuario.plano_trabalho.id
        return reverse_lazy('planotrabalho:planotrabalho', args=[trabalho])


class CadastrarOrgaoGestor(CreateView):
    form_class = OrgaoGestorForm
    template_name = 'planotrabalho/cadastrar_orgao.html'

    def get_form_kwargs(self):
        kwargs = super(CadastrarOrgaoGestor, self).get_form_kwargs()
        kwargs['user'] = self.request.user.usuario
        return kwargs

    def form_valid(self, form):
        self.request.user.usuario.plano_trabalho.orgao_gestor = form.save()
        self.request.user.usuario.plano_trabalho.save()
        return super(CadastrarOrgaoGestor, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        orgao = self.request.user.usuario.plano_trabalho.orgao_gestor
        if orgao:
            return redirect('planotrabalho:alterar_gestor', pk=orgao.id)

        return super(CadastrarOrgaoGestor, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        trabalho = self.request.user.usuario.plano_trabalho.id
        return reverse_lazy('planotrabalho:planotrabalho', args=[trabalho])


class AlterarOrgaoGestor(UpdateView):
    form_class = OrgaoGestorForm
    model = OrgaoGestor
    template_name = 'planotrabalho/cadastrar_orgao.html'

    def get_form_kwargs(self):
        kwargs = super(AlterarOrgaoGestor, self).get_form_kwargs()
        kwargs['user'] = self.request.user.usuario
        return kwargs

    def get_success_url(self):
        trabalho = self.request.user.usuario.plano_trabalho.id
        return reverse_lazy('planotrabalho:planotrabalho', args=[trabalho])


class CadastrarConselho(CreateView):
    form_class = ConselhoCulturalForm
    template_name = 'planotrabalho/cadastrar_conselho.html'

    def get_form_kwargs(self):
        kwargs = super(CadastrarConselho, self).get_form_kwargs()
        kwargs['user'] = self.request.user.usuario
        return kwargs

    def form_valid(self, form):
        self.request.user.usuario.plano_trabalho.conselho_cultural = form.save()
        self.request.user.usuario.plano_trabalho.save()
        return super(CadastrarConselho, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        conselho = self.request.user.usuario.plano_trabalho.conselho_cultural
        if conselho:
            return redirect('planotrabalho:alterar_conselho', pk=conselho.id)

        return super(CadastrarConselho, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        trabalho = self.request.user.usuario.plano_trabalho.id
        return reverse_lazy('planotrabalho:planotrabalho', args=[trabalho])


class AlterarConselho(UpdateView):
    form_class = ConselhoCulturalForm
    model = ConselhoCultural
    template_name = 'planotrabalho/cadastrar_conselho.html'

    def get_form_kwargs(self):
        kwargs = super(AlterarConselho, self).get_form_kwargs()
        kwargs['user'] = self.request.user.usuario
        return kwargs

    def get_success_url(self):
        trabalho = self.request.user.usuario.plano_trabalho.id
        return reverse_lazy('planotrabalho:planotrabalho', args=[trabalho])


def get_conselheiros(request):
    if request.is_ajax() and request.GET.get('id', None):
        pk = request.GET.get('id')
        conselheiros = Conselheiro.objects.filter(conselho__pk=pk)
        response = {}
        response['conselheiros'] = list(conselheiros.values_list('nome', 'email', 'segmento'))
        return HttpResponse(
            json.dumps(response),
            content_type="application/json")
    else:
        return Http404()


class CadastrarFundo(CreateView):
    form_class = FundoCulturaForm
    template_name = 'planotrabalho/cadastrar_fundo.html'

    def get_form_kwargs(self):
        kwargs = super(CadastrarFundo, self).get_form_kwargs()
        kwargs['user'] = self.request.user.usuario
        return kwargs

    def form_valid(self, form):
        self.request.user.usuario.plano_trabalho.fundo_cultura = form.save()
        self.request.user.usuario.plano_trabalho.save()
        return super(CadastrarFundo, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        fundo = self.request.user.usuario.plano_trabalho.fundo_cultura
        if fundo:
            return redirect('planotrabalho:alterar_fundo', pk=fundo.id)

        return super(CadastrarFundo, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        trabalho = self.request.user.usuario.plano_trabalho.id
        return reverse_lazy('planotrabalho:planotrabalho', args=[trabalho])


class AlterarFundo(UpdateView):
    form_class = FundoCulturaForm
    model = FundoCultura
    template_name = 'planotrabalho/cadastrar_fundo.html'

    def get_form_kwargs(self):
        kwargs = super(AlterarFundo, self).get_form_kwargs()
        kwargs['user'] = self.request.user.usuario
        return kwargs

    def get_success_url(self):
        trabalho = self.request.user.usuario.plano_trabalho.id
        return reverse_lazy('planotrabalho:planotrabalho', args=[trabalho])


class CadastrarPlano(CreateView):
    form_class = PlanoCulturaForm
    template_name = 'planotrabalho/cadastrar_plano.html'

    def get_form_kwargs(self):
        kwargs = super(CadastrarPlano, self).get_form_kwargs()
        kwargs['user'] = self.request.user.usuario
        return kwargs

    def form_valid(self, form):
        self.request.user.usuario.plano_trabalho.plano_cultura = form.save()
        self.request.user.usuario.plano_trabalho.save()
        return super(CadastrarPlano, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        plano = self.request.user.usuario.plano_trabalho.plano_cultura
        if plano:
            return redirect('planotrabalho:alterar_plano', pk=plano.id)

        return super(CadastrarPlano, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        trabalho = self.request.user.usuario.plano_trabalho.id
        return reverse_lazy('planotrabalho:planotrabalho', args=[trabalho])


class AlterarPlano(UpdateView):
    form_class = PlanoCulturaForm
    model = PlanoCultura
    template_name = 'planotrabalho/cadastrar_plano.html'

    def get_form_kwargs(self):
        kwargs = super(AlterarPlano, self).get_form_kwargs()
        kwargs['user'] = self.request.user.usuario
        return kwargs

    def get_success_url(self):
        trabalho = self.request.user.usuario.plano_trabalho
        return reverse_lazy('planotrabalho:planotrabalho', args=[trabalho])
