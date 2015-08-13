from datetime import timedelta
from threading import Thread

from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError

from adesao.models import Municipio, Responsavel, Secretario, Usuario, Historico
from adesao.forms import CadastrarUsuarioForm, CadastrarMunicipioForm
from adesao.forms import CadastrarResponsavelForm, CadastrarSecretarioForm
from adesao.utils import enviar_email_conclusao

from wkhtmltopdf.views import PDFTemplateView


# Create your views here.
def index(request):
    if request.user.is_authenticated():
        return redirect('adesao:home')
    return render(request, 'index.html')


def fale_conosco(request):
    return render(request, 'fale_conosco.html')


@login_required
def home(request):
    ente_federado = request.user.usuario.municipio
    secretario = request.user.usuario.secretario
    responsavel = request.user.usuario.responsavel
    situacao = request.user.usuario.estado_processo
    historico = Historico.objects.filter(usuario=request.user.usuario)
    historico = historico.order_by('-data_alteracao')

    if request.user.is_staff:
        return redirect('gestao:acompanhar_adesao')

    if ente_federado and secretario and responsavel and int(situacao) < 1:
        request.user.usuario.estado_processo = '1'
        request.user.usuario.save()
        message_txt = render_to_string('conclusao_cadastro.txt',
                                       {'request': request})
        message_html = render_to_string('conclusao_cadastro.email',
                                        {'request': request})
        enviar_email_conclusao(request.user, message_txt, message_html)
    return render(request, 'home.html', {'historico': historico})


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


def sucesso_usuario(request):
    return render(request, 'usuario/mensagem_sucesso.html')


def sucesso_responsavel(request):
    return render(request, 'responsavel/mensagem_sucesso.html')


class CadastrarUsuario(CreateView):
    form_class = CadastrarUsuarioForm
    template_name = 'usuario/cadastrar_usuario.html'
    success_url = reverse_lazy('adesao:sucesso_usuario')

    def get_success_url(self):
        Thread(target=send_mail, args=(
            'MINISTÉRIO DA CULTURA - SNC - CREDENCIAIS DE ACESSO',
            'Prezad@ ' + self.object.usuario.nome_usuario + ',\n' +
            'Recebemos o seu cadastro no Sistema Nacional de Cultura. ' +
            'Por favor confirme seu e-mail clicando no endereço abaixo:\n\n' +
            self.request.build_absolute_uri(reverse(
                'adesao:ativar_usuario',
                args=[self.object.usuario.codigo_ativacao])) + '\n\n' +
            'Atenciosamente,\n\n' +
            'Equipe SNC\nMinistério da Cultura',
            'naoresponda@cultura.gov.br',
            [self.object.email],),
            kwargs = {'fail_silently': 'False', }
        ).start()
        return super(CadastrarUsuario, self).get_success_url()


@login_required
def selecionar_tipo_ente(request):
    return render(request, 'prefeitura/selecionar_tipo_ente.html')


def sucesso_municipio(request):
    return render(request, 'prefeitura/mensagem_sucesso_prefeitura.html')


class CadastrarMunicipio(CreateView):
    form_class = CadastrarMunicipioForm
    template_name = 'prefeitura/cadastrar_prefeitura.html'
    success_url = reverse_lazy('adesao:sucesso_municipio')

    def get_context_data(self, **kwargs):
        context = super(CadastrarMunicipio, self).get_context_data(**kwargs)
        context['tipo_ente'] = self.kwargs['tipo_ente']
        return context

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
    success_url = reverse_lazy('adesao:sucesso_municipio')

    def dispatch(self, *args, **kwargs):
        municipio = self.request.user.usuario.municipio.pk
        if str(municipio) != self.kwargs['pk']:
            raise Http404()

        return super(AlterarMunicipio, self).dispatch(*args, **kwargs)


class CadastrarResponsavel(CreateView):
    form_class = CadastrarResponsavelForm
    template_name = 'responsavel/cadastrar_responsavel.html'
    success_url = reverse_lazy('adesao:sucesso_responsavel')

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


@login_required
def importar_secretario(request):
    secretario = request.user.usuario.secretario
    # TODO: Refatorar essa importação depois que a migração for realizada
    responsavel = Responsavel()
    if secretario:
        responsavel.cpf_responsavel = secretario.cpf_secretario
        responsavel.rg_responsavel = secretario.rg_secretario
        responsavel.orgao_expeditor_rg = secretario.orgao_expeditor_rg
        responsavel.estado_expeditor = secretario.estado_expeditor
        responsavel.nome_responsavel = secretario.nome_secretario
        responsavel.cargo_responsavel = secretario.cargo_secretario
        responsavel.instituicao_responsavel = secretario.instituicao_secretario
        responsavel.telefone_um = secretario.telefone_um
        responsavel.telefone_dois = secretario.telefone_dois
        responsavel.telefone_tres = secretario.telefone_tres
        responsavel.email_institucional_responsavel = secretario.email_institucional_secretario
        try:
            responsavel.full_clean()
            responsavel.save()
        except ValidationError:
            return redirect('adesao:responsavel')
        request.user.usuario.responsavel = responsavel
        request.user.usuario.save()
    return redirect('adesao:responsavel')


class AlterarCadastrador(UpdateView):
    form_class = CadastrarResponsavelForm
    model = Responsavel
    template_name = 'responsavel/cadastrar_responsavel.html'
    success_url = reverse_lazy('adesao:alteracao')


class AlterarResponsavel(UpdateView):
    form_class = CadastrarResponsavelForm
    model = Responsavel
    template_name = 'responsavel/cadastrar_responsavel.html'
    success_url = reverse_lazy('adesao:sucesso_responsavel')


def sucesso_secretario(request):
    return render(request, 'secretario/mensagem_sucesso_secretario.html')


class CadastrarSecretario(CreateView):
    form_class = CadastrarSecretarioForm
    template_name = 'secretario/cadastrar_secretario.html'
    success_url = reverse_lazy('adesao:sucesso_secretario')

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
        success_url = reverse_lazy('adesao:sucesso_secretario')


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


class OficioAlteracao(PDFTemplateView):
    filename = 'alterar_responsavel.pdf'
    template_name = 'termos/alterar_responsavel.html'
    show_content_in_browser = True

    def get_context_data(self, **kwargs):
        context = super(OficioAlteracao, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['static'] = self.request.get_host()
        return context
