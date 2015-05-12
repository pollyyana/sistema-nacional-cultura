from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy

from adesao.models import Municipio, Responsavel, Secretario, Usuario


# Create your views here.
def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


class CadastrarUsuario(CreateView):
    model = Usuario
    fields = [
        'user',
        'nome_usuario',
        'email_usuario'
    ]
    template_name = 'usuario/cadastrar_usuario.html'
    success_url = reverse_lazy('index')


class CadastrarMunicipio(CreateView):
    model = Municipio
    fields = [
        'cpf_prefeito',
        'nome_prefeito',
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


def alterar_prefeitura(request, prefeitura_id):
    return render(request, 'prefeitura/cadastrar.html')


class CadastrarResponsavel(CreateView):
    model = Responsavel
    fields = [
        'cpf_responsavel',
        'nome_responsavel',
        'cargo_responsavel',
        'instituicao_responsavel',
        'telefone_um',
        'telefone_dois',
        'telefone_tres',
        'email_institucional_responsavel'
    ]
    template_name = 'responsavel/cadastrar_responsavel.html'
    success_url = reverse_lazy('adesao:secretario')


def alterar_responsavel(request, responsavel_id):
    return render(request, 'responsavel/cadastrar.html')


class CadastrarSecretario(CreateView):
    model = Secretario
    fields = [
        'cpf_secretario',
        'nome_secretario',
        'cargo_secretario',
        'instituicao_secretario',
        'telefone_um',
        'telefone_dois',
        'telefone_tres',
        'email_institucional_secretario'
    ]
    template_name = 'secretario/cadastrar_secretario.html'
    success_url = reverse_lazy('adesao:index')


def alterar_secretario(request, secretario_id):
    return render(request, 'secretario/cadastrar.html')
