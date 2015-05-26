from datetime import timedelta

from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from adesao.models import Municipio, Responsavel, Secretario, Usuario
from adesao.forms import CadastrarUsuarioForm, CadastrarMunicipioForm
from adesao.forms import CadastrarResponsavelForm, CadastrarSecretarioForm

from wkhtmltopdf.views import PDFTemplateView


# Create your views here.
def index(request):
    return render(request, 'index.html')


@login_required
def home(request):
    return render(request, 'home.html')


def ativar_usuario(request, codigo):
    usuario = Usuario.objects.get(codigo_ativacao=codigo)

    if usuario is None:
        raise Http404()

    if timezone.now() > (usuario.data_cadastro + timedelta(days=3)):
        raise Http404()

    usuario.user.is_active = True
    usuario.save()
    usuario.user.save()

    return render(request, 'confirmar_email.html')


class CadastrarUsuario(CreateView):
    form_class = CadastrarUsuarioForm
    template_name = 'usuario/cadastrar_usuario.html'
    success_url = reverse_lazy('adesao:index')


class CadastrarMunicipio(FormView):
    form_class = CadastrarMunicipioForm
    template_name = 'prefeitura/cadastrar_prefeitura.html'
    success_url = reverse_lazy('adesao:responsavel')

    def form_valid(self, form):
        self.request.user.usuario.municipio = form.save(commit=True)
        self.request.user.usuario.save()
        return super(CadastrarMunicipio, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        municipio = self.request.user.usuario.municipio
        if municipio:
            return redirect('adesao:alterar_municipio', pk=municipio.id)

        return super(CadastrarMunicipio, self).dispatch(*args, **kwargs)


class AlterarMunicipio(UpdateView):
    form_class = CadastrarMunicipioForm
    model = Municipio
    template_name = 'prefeitura/cadastrar_prefeitura.html'
    success_url = reverse_lazy('adesao:responsavel')

    def dispatch(self, *args, **kwargs):
        municipio = self.request.user.usuario.municipio.pk
        print(municipio)
        print(self.kwargs['pk'])
        if str(municipio) != self.kwargs['pk']:
            raise Http404()
            # return redirect('adesao:alterar_municipio', pk=municipio)

        return super(AlterarMunicipio, self).dispatch(*args, **kwargs)


class CadastrarResponsavel(CreateView):
    form_class = CadastrarResponsavelForm
    template_name = 'responsavel/cadastrar_responsavel.html'
    success_url = reverse_lazy('adesao:home')

    def form_valid(self, form):
        self.request.user.usuario.responsavel = form.save(commit=True)
        self.request.user.usuario.save()
        return super(CadastrarResponsavel, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        responsavel = self.request.user.usuario.responsavel
        if responsavel:
            return redirect(
                'adesao:alterar_responsavel',
                pk=responsavel.id)

        return super(CadastrarResponsavel, self).dispatch(*args, **kwargs)


class AlterarResponsavel(UpdateView):
    form_class = CadastrarResponsavelForm
    model = Responsavel
    template_name = 'responsavel/cadastrar_responsavel.html'
    success_url = reverse_lazy('adesao:home')


class CadastrarSecretario(CreateView):
    form_class = CadastrarSecretarioForm
    template_name = 'secretario/cadastrar_secretario.html'
    success_url = reverse_lazy('adesao:responsavel')

    def form_valid(self, form):
        self.request.user.usuario.secretario = form.save(commit=True)
        self.request.user.usuario.save()
        return super(CadastrarSecretario, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        secretario = self.request.user.usuario.secretario
        if secretario:
            return redirect('adesao:alterar_secretario', pk=secretario.id)

        return super(CadastrarSecretario, self).dispatch(*args, **kwargs)


class AlterarSecretario(UpdateView):
        form_class = CadastrarSecretarioForm
        model = Secretario
        template_name = 'secretario/cadastrar_secretario.html'
        success_url = reverse_lazy('adesao:responsavel')


class MinutaAcordo(PDFTemplateView):
    filename = 'minuta_acordo.pdf'
    header_template = 'termos/minuta_header.html'
    template_name = 'termos/minuta_acordo.html'
    show_content_in_browser = True
    cmd_options = {
        'margin-top': 60,
        'header-spacing': 5,
    }

    def get_context_data(self, **kwargs):
        context = super(MinutaAcordo, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context


class TermoSolicitacao(PDFTemplateView):
    filename = 'solicitacao.pdf'
    header_template = 'termos/solicitacao_header.html'
    template_name = 'termos/solicitacao.html'
    show_content_in_browser = True
    cmd_options = {
        'margin-top': 40,
        'header-spacing': 5,
    }

    def get_context_data(self, **kwargs):
        context = super(TermoSolicitacao, self).get_context_data(**kwargs)
        context['request'] = self.request
        return context
