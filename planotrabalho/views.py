from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse_lazy

from planotrabalho.models import PlanoTrabalho, CriacaoSistema, OrgaoGestor
from planotrabalho.models import ConselhoCultural, FundoCultura, PlanoCultura
from .forms import CriarSistemaForm, OrgaoGestorForm, ConselhoCulturalForm
from .forms import FundoCulturaForm, PlanoCulturaForm


# Create your views here.
class PlanoTrabalho(DetailView):
    model = PlanoTrabalho
    template_name = 'planotrabalho/plano_trabalho.html'


class CadastrarSistema(CreateView):
    form_class = CriarSistemaForm
    template_name = 'planotrabalho/cadastrar_sistema.html'
    success_url = reverse_lazy('planotrabalho:gestor')

    def form_valid(self, form):
        self.request.user.usuario.plano_trabalho.criacao_sistema = form.save()
        self.request.user.usuario.plano_trabalho.save()
        return super(CadastrarSistema, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        sistema = self.request.user.usuario.plano_trabalho.criacao_sistema
        if sistema:
            return redirect('planotrabalho:alterar_sistema', pk=sistema.id)

        return super(CadastrarSistema, self).dispatch(*args, **kwargs)


class AlterarSistema(UpdateView):
    form_class = CriarSistemaForm
    model = CriacaoSistema
    template_name = 'planotrabalho/cadastrar_sistema.html'
    success_url = reverse_lazy('planotrabalho:gestor')


class CadastrarOrgaoGestor(CreateView):
    form_class = OrgaoGestorForm
    template_name = 'planotrabalho/cadastrar_orgao.html'
    success_url = reverse_lazy('planotrabalho:conselho')

    def form_valid(self, form):
        self.request.user.usuario.plano_trabalho.orgao_gestor = form.save()
        self.request.user.usuario.plano_trabalho.save()
        return super(CadastrarOrgaoGestor, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        orgao = self.request.user.usuario.plano_trabalho.orgao_gestor
        if orgao:
            return redirect('planotrabalho:alterar_gestor', pk=orgao.id)

        return super(CadastrarOrgaoGestor, self).dispatch(*args, **kwargs)


class AlterarOrgaoGestor(UpdateView):
    form_class = OrgaoGestorForm
    model = OrgaoGestor
    template_name = 'planotrabalho/cadastrar_orgao.html'
    success_url = reverse_lazy('planotrabalho:conselho')


class CadastrarConselho(CreateView):
    form_class = ConselhoCulturalForm
    template_name = 'planotrabalho/cadastrar_conselho.html'
    success_url = reverse_lazy('planotrabalho:fundo')

    def form_valid(self, form):
        self.request.user.usuario.plano_trabalho.conselho_cultural = form.save()
        self.request.user.usuario.plano_trabalho.save()
        return super(CadastrarConselho, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        conselho = self.request.user.usuario.plano_trabalho.conselho_cultural
        if conselho:
            return redirect('planotrabalho:alterar_conselho', pk=conselho.id)

        return super(CadastrarConselho, self).dispatch(*args, **kwargs)


class AlterarConselho(UpdateView):
    form_class = ConselhoCulturalForm
    model = ConselhoCultural
    template_name = 'planotrabalho/cadastrar_conselho.html'
    success_url = reverse_lazy('planotrabalho:fundo')


class CadastrarFundo(CreateView):
    form_class = FundoCulturaForm
    template_name = 'planotrabalho/cadastrar_fundo.html'
    success_url = reverse_lazy('planotrabalho:plano')

    def form_valid(self, form):
        self.request.user.usuario.plano_trabalho.fundo_cultura = form.save()
        self.request.user.usuario.plano_trabalho.save()
        return super(CadastrarFundo, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        fundo = self.request.user.usuario.plano_trabalho.fundo_cultura
        if fundo:
            return redirect('planotrabalho:alterar_fundo', pk=fundo.id)

        return super(CadastrarFundo, self).dispatch(*args, **kwargs)


class AlterarFundo(UpdateView):
    form_class = FundoCulturaForm
    model = FundoCultura
    template_name = 'planotrabalho/cadastrar_fundo.html'
    success_url = reverse_lazy('planotrabalho:plano')


class CadastrarPlano(CreateView):
    form_class = PlanoCulturaForm
    template_name = 'planotrabalho/cadastrar_plano.html'

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

    def get_success_url(self):
        trabalho = self.request.user.usuario.plano_trabalho
        return reverse_lazy('planotrabalho:planotrabalho', args=[trabalho])
