from datetime import timedelta
from threading import Thread

from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from adesao.models import Municipio, Responsavel, Secretario, Usuario
from adesao.forms import CadastrarUsuarioForm, CadastrarMunicipioForm
from adesao.forms import CadastrarResponsavelForm, CadastrarSecretarioForm

from wkhtmltopdf.views import PDFTemplateView


# Create your views here.
def index(request):
    if request.user.is_authenticated():
        return render(request, 'home.html')
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

    def get_success_url(self):
        Thread(target=send_mail, args=(
            'MINISTÉRIO DA CULTURA - SNC - CREDENCIAIS DE ACESSO',
            'Prezado '+self.object.username+',\n' +
            'Recebemos o seu cadastro no Sistema Nacional de Cultura.' +
            'Por favor confirme seu e-mail clicando no endereço abaixo:\n\n' +
            self.request.build_absolute_uri(reverse(
                'adesao:ativar_usuario',
                args=[self.object.usuario.codigo_ativacao]))+'\n\n' +
            'Atenciosamente,\n\n' +
            'Equipe SAI - Ministério da Cultura',
            '',
            [self.object.email],),
            kwargs = {'fail_silently': 'False', }
        ).start()
        return super(CadastrarUsuario, self).get_success_url()


class CadastrarMunicipio(CreateView):
    form_class = CadastrarMunicipioForm
    template_name = 'prefeitura/cadastrar_prefeitura.html'
    success_url = reverse_lazy('adesao:home')

    def form_valid(self, form):
        self.request.user.usuario.municipio = form.save()
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
    success_url = reverse_lazy('adesao:home')

    def dispatch(self, *args, **kwargs):
        municipio = self.request.user.usuario.municipio.pk
        if str(municipio) != self.kwargs['pk']:
            raise Http404()

        return super(AlterarMunicipio, self).dispatch(*args, **kwargs)


class CadastrarResponsavel(CreateView):
    form_class = CadastrarResponsavelForm
    template_name = 'responsavel/cadastrar_responsavel.html'
    success_url = reverse_lazy('adesao:home')

    def form_valid(self, form):
        self.request.user.usuario.responsavel = form.save()
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
    success_url = reverse_lazy('adesao:home')

    def form_valid(self, form):
        self.request.user.usuario.secretario = form.save()
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
        success_url = reverse_lazy('adesao:home')


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
        context['static'] = self.request.get_host()
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
        context['static'] = self.request.get_host()
        return context
