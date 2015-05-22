from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required

from adesao.models import Municipio, Responsavel, Secretario
from adesao.forms import CadastrarUsuarioForm, CadastrarMunicipioForm
from adesao.forms import CadastrarResponsavelForm, CadastrarSecretarioForm

from wkhtmltopdf.views import PDFTemplateView


# Create your views here.
def index(request):
    return render(request, 'index.html')


@login_required
def home(request):
    return render(request, 'home.html')


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
            return redirect('alterar_municipio', municipio_id=municipio.id)

        return super(CadastrarMunicipio, self).dispatch(*args, **kwargs)


class AlterarMunicipio(UpdateView):
    form_class = CadastrarMunicipioForm
    model = Municipio
    template_name = 'prefeitura/cadastrar_prefeitura.html'
    success_url = reverse_lazy('adesao:responsavel')


class CadastrarResponsavel(CreateView):
    form_class = CadastrarResponsavelForm
    template_name = 'responsavel/cadastrar_responsavel.html'
    success_url = reverse_lazy('adesao:index')

    def form_valid(self, form):
        self.request.user.usuario.responsavel = form.save(commit=True)
        self.request.user.usuario.save()
        return super(CadastrarResponsavel, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        responsavel = self.request.user.usuario.responsavel
        if responsavel:
            return redirect(
                'alterar_responsavel',
                responsavel_id=responsavel.id)

        return super(CadastrarResponsavel, self).dispatch(*args, **kwargs)


class AlterarResponsavel(UpdateView):
    form_class = CadastrarResponsavelForm
    model = Responsavel
    template_name = 'responsavel/cadastrar_responsavel.html'
    success_url = reverse_lazy('adesao:index')


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
            return redirect('alterar_secretario', secretario_id=secretario.id)

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
