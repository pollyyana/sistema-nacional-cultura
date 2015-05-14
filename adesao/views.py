from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy

from adesao.models import Municipio, Responsavel, Secretario
from adesao.forms import CadastrarUsuarioForm


# Create your views here.
def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


class CadastrarUsuario(CreateView):
    form_class = CadastrarUsuarioForm
    template_name = 'usuario/cadastrar_usuario.html'
    success_url = reverse_lazy('adesao:index')


class CadastrarMunicipio(CreateView):
    model = Municipio
    fields = [
        'cpf_prefeito',
        'nome_prefeito',
        'rg_prefeito',
        'orgao_expeditor_rg',
        'estado_expeditor',
        'cnpj_prefeitura',
        'endereco',
        'complemento',
        'cep',
        'bairro',
        'cidade',
        'estado',
        'telefone_um',
        'telefone_dois',
        'telefone_tres',
        'email_institucional_prefeito'
    ]
    template_name = 'prefeitura/cadastrar_prefeitura.html'
    success_url = reverse_lazy('adesao:responsavel')

    def dispatch(self, *args, **kwargs):
        municipio = self.request.user.usuario.municipio
        if municipio:
            return redirect('alterar_municipio', municipio_id=municipio.id)

        return super(CadastrarMunicipio, self).dispatch(*args, **kwargs)


class AlterarMunicipio(UpdateView):
    model = Municipio
    fields = [
        'cpf_prefeito',
        'nome_prefeito',
        'rg_prefeito',
        'orgao_expeditor_rg',
        'estado_expeditor',
        'cnpj_prefeitura',
        'endereco',
        'complemento',
        'cep',
        'bairro',
        'cidade',
        'estado',
        'telefone_um',
        'telefone_dois',
        'telefone_tres',
        'email_institucional_prefeito'
    ]
    template_name = 'prefeitura/cadastrar_prefeitura.html'
    success_url = reverse_lazy('adesao:responsavel')


class CadastrarResponsavel(CreateView):
    model = Responsavel
    fields = [
        'cpf_responsavel',
        'nome_responsavel',
        'rg_responsavel',
        'orgao_expeditor_rg',
        'estado_expeditor',
        'cargo_responsavel',
        'instituicao_responsavel',
        'telefone_um',
        'telefone_dois',
        'telefone_tres',
        'email_institucional_responsavel'
    ]
    template_name = 'responsavel/cadastrar_responsavel.html'
    success_url = reverse_lazy('adesao:index')

    def dispatch(self, *args, **kwargs):
        responsavel = self.request.user.usuario.responsavel
        if responsavel:
            return redirect(
                'alterar_responsavel',
                responsavel_id=responsavel.id)

        return super(CadastrarResponsavel, self).dispatch(*args, **kwargs)


class AlterarResponsavel(UpdateView):
    model = Responsavel
    fields = [
        'cpf_responsavel',
        'nome_responsavel',
        'rg_responsavel',
        'orgao_expeditor_rg',
        'estado_expeditor',
        'cargo_responsavel',
        'instituicao_responsavel',
        'telefone_um',
        'telefone_dois',
        'telefone_tres',
        'email_institucional_responsavel'
    ]
    template_name = 'responsavel/cadastrar_responsavel.html'
    success_url = reverse_lazy('adesao:index')


class CadastrarSecretario(CreateView):
    model = Secretario
    fields = [
        'cpf_secretario',
        'nome_secretario',
        'rg_secretario',
        'orgao_expeditor_rg',
        'estado_expeditor',
        'cargo_secretario',
        'instituicao_secretario',
        'telefone_um',
        'telefone_dois',
        'telefone_tres',
        'email_institucional_secretario'
    ]
    template_name = 'secretario/cadastrar_secretario.html'
    success_url = reverse_lazy('adesao:responsavel')

    def dispatch(self, *args, **kwargs):
        secretario = self.request.user.usuario.secretario
        if secretario:
            return redirect('alterar_secretario', secretario_id=secretario.id)

        return super(CadastrarSecretario, self).dispatch(*args, **kwargs)


class AlterarSecretario(UpdateView):
        model = Secretario
        fields = [
            'cpf_secretario',
            'nome_secretario',
            'rg_secretario',
            'orgao_expeditor_rg',
            'estado_expeditor',
            'cargo_secretario',
            'instituicao_secretario',
            'telefone_um',
            'telefone_dois',
            'telefone_tres',
            'email_institucional_secretario'
        ]
        template_name = 'secretario/cadastrar_secretario.html'
        success_url = reverse_lazy('adesao:responsavel')
