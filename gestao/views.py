from django.shortcuts import redirect, render
from django.http import Http404
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, UpdateView

from adesao.models import Usuario, Cidade, Municipio
from planotrabalho.models import CriacaoSistema, PlanoCultura, FundoCultura, OrgaoGestor, ConselhoCultural

from .forms import AlterarSituacao, DiligenciaForm, AlterarDocumentosEnteFederadoForm
from .forms import AlterarCadastradorForm, AlterarUsuarioForm, AlterarOrgaoForm
from .forms import AlterarFundoForm, AlterarPlanoForm, AlterarConselhoForm, AlterarSistemaForm
from .forms import ProrrogacaoFundoForm, ProrrogacaoConselhoForm
from .forms import ProrrogacaoSistemaForm, ProrrogacaoOrgaoForm, ProrrogacaoPlanoForm

from clever_selects.views import ChainedSelectChoicesView


# Acompanhamento das adesões
class AlterarCadastrador(FormView):
    template_name = 'gestao/alterar_cadastrador.html'
    form_class = AlterarCadastradorForm
    success_url = reverse_lazy('gestao:acompanhar_adesao')

    def form_valid(self, form):
        form.save()
        return super(AlterarCadastrador, self).form_valid(form)


class AlterarCadastradorEstado(FormView):
    template_name = 'gestao/alterar_cadastrador_estado.html'
    form_class = AlterarCadastradorForm
    success_url = reverse_lazy('gestao:acompanhar_adesao')

    def form_valid(self, form):
        form.save()
        return super(AlterarCadastradorEstado, self).form_valid(form)


class MunicipioChain(ChainedSelectChoicesView):
    def get_choices(self):
        data = Cidade.objects.filter(uf=self.parent_value)
        choices = []
        for cidade in data:
            choices.append((str(cidade.id), cidade.nome_municipio))
        return choices


def alterar_situacao(request, id):
    if request.method == "POST":
        form = AlterarSituacao(
            request.POST,
            instance=Usuario.objects.get(id=id))
        if form.is_valid():
            form.save()
    return redirect('gestao:acompanhar_adesao')


class AcompanharPrazo(ListView):
    template_name = 'gestao/acompanhar_prazo.html'
    paginate_by = 10

    def get_queryset(self):
        ente_federado = self.request.GET.get('municipio', None)
        if ente_federado:
            municipio = Usuario.objects.filter(
                municipio__cidade__nome_municipio__icontains=ente_federado)
            estado = Usuario.objects.filter(
                municipio__cidade__isnull=True,
                municipio__estado__nome_uf__icontains=ente_federado)

            return municipio | estado
        return Usuario.objects.filter(prazo=2, estado_processo='6', data_publicacao_acordo__isnull=False)


def aditivar_prazo(request, id):
    if request.method == "POST":
        user = Usuario.objects.get(id=id)
        user.prazo = 4
        user.save()
    return redirect('gestao:acompanhar_prazo')


class AcompanharAdesao(ListView):
    template_name = 'gestao/adesao/acompanhar.html'
    paginate_by = 10

    def get_queryset(self):
        situacao = self.request.GET.get('situacao', None)
        ente_federado = self.request.GET.get('municipio', None)

        if situacao in ('1', '2', '3', '4', '5'):
            return Municipio.objects.filter(usuario__estado_processo=situacao)

        if ente_federado:
            municipio = Municipio.objects.filter(
                cidade__nome_municipio__icontains=ente_federado)
            estado = Municipio.objects.filter(
                cidade__nome_municipio__isnull=True,
                estado__nome_uf__icontains=ente_federado)

            return municipio | estado

        return Municipio.objects.filter(usuario__estado_processo__range=('1', '5'))


# Acompanhamento dos planos de trabalho
def diligencia_documental(request, etapa, st, id):
    usuario = Usuario.objects.get(id=id)
    setattr(getattr(usuario.plano_trabalho, etapa), st, 0)
    form = DiligenciaForm()
    if request.method == 'POST':
        form = DiligenciaForm(request.POST, usuario=usuario)
        if form.is_valid():
            getattr(usuario.plano_trabalho, etapa).save()
            form.save()
        return redirect('gestao:acompanhar_adesao')
    return render(
        request,
        'gestao/planotrabalho/diligencia.html',
        {'form': form, 'etapa': etapa, 'st': st, 'id': id})


def concluir_etapa(request, etapa, st, id):
    usuario = Usuario.objects.get(id=id)
    setattr(getattr(usuario.plano_trabalho, etapa), st, 2)
    getattr(usuario.plano_trabalho, etapa).save()
    return redirect('gestao:acompanhar_adesao')


class AcompanharSistema(ListView):
    template_name = 'gestao/planotrabalho/acompanhar_sistema.html'
    paginate_by = 10

    def get_queryset(self):
        anexo = self.request.GET.get('anexo', None)
        q = self.request.GET.get('q', None)
        if not anexo:
            raise Http404()
        usuarios = Usuario.objects.filter(estado_processo='6')
        usuarios = usuarios.exclude(plano_trabalho__criacao_sistema=None)

        if anexo == 'minuta_projeto_lei':
            usuarios = usuarios.filter(
                plano_trabalho__criacao_sistema__situacao_minuta=1)
        elif anexo == 'lei_sistema_cultura':
            usuarios = usuarios.filter(
                plano_trabalho__criacao_sistema__situacao_lei_sistema=1)
        else:
            raise Http404()

        if q:
            usuarios = usuarios.filter(
                municipio__cidade__nome_municipio__icontains=q)

        return usuarios


class AcompanharOrgao(ListView):
    template_name = 'gestao/planotrabalho/acompanhar_orgao.html'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        usuarios = Usuario.objects.filter(estado_processo='6')
        usuarios = usuarios.exclude(plano_trabalho__orgao_gestor=None)
        usuarios = usuarios.filter(
            plano_trabalho__orgao_gestor__situacao_relatorio_secretaria=1)
        if q:
            usuarios = usuarios.filter(
                municipio__cidade__nome_municipio__icontains=q)
        return usuarios


class AcompanharConselho(ListView):
    template_name = 'gestao/planotrabalho/acompanhar_conselho.html'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        usuarios = Usuario.objects.filter(estado_processo='6')
        usuarios = usuarios.exclude(plano_trabalho__conselho_cultural=None)
        usuarios = usuarios.filter(
            plano_trabalho__conselho_cultural__situacao_ata=1)
        if q:
            usuarios = usuarios.filter(
                municipio__cidade__nome_municipio__icontains=q)
        return usuarios


class AcompanharFundo(ListView):
    template_name = 'gestao/planotrabalho/acompanhar_fundo.html'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        usuarios = Usuario.objects.filter(estado_processo='6')
        usuarios = usuarios.exclude(plano_trabalho__fundo_cultura=None)
        usuarios = usuarios.filter(
            plano_trabalho__fundo_cultura__situacao_lei_plano=1)
        if q:
            usuarios = usuarios.filter(
                municipio__cidade__nome_municipio__icontains=q)
        return usuarios


class AcompanharPlano(ListView):
    template_name = 'gestao/planotrabalho/acompanhar_plano.html'
    paginate_by = 10

    def get_queryset(self):
        anexo = self.request.GET.get('anexo', None)
        q = self.request.GET.get('q', None)
        if not anexo:
            raise Http404()
        usuarios = Usuario.objects.filter(estado_processo='6')
        usuarios = usuarios.exclude(plano_trabalho__plano_cultura=None)

        if anexo == 'relatorio_diretrizes_aprovadas':
            usuarios = usuarios.filter(
                plano_trabalho__plano_cultura__situacao_relatorio_diretrizes=1)
        elif anexo == 'minuta_preparada':
            usuarios = usuarios.filter(
                plano_trabalho__plano_cultura__situacao_minuta=1)
        elif anexo == 'ata_reuniao_aprovacao_plano':
            usuarios = usuarios.filter(
                plano_trabalho__plano_cultura__situacao_ata=1)
        elif anexo == 'lei_plano_cultura':
            usuarios = usuarios.filter(
                plano_trabalho__plano_cultura__situacao_lei_plano=1)
        else:
            raise Http404()

        if q:
            usuarios = usuarios.filter(
                municipio__cidade__nome_municipio__icontains=q)

        return usuarios


class DetalharUsuario(DetailView):
    model = Usuario
    template_name = 'gestao/detalhe_municipio.html'


class ListarUsuarios(ListView):
    model = Usuario
    template_name = 'gestao/listar_usuarios.html'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        usuarios = Usuario.objects.all()

        if q:
            usuarios = usuarios.filter(Q(user__username__icontains=q) | Q(user__email__icontains=q))

        return usuarios


class AlterarUsuario(UpdateView):
    model = User
    form_class = AlterarUsuarioForm
    template_name = 'gestao/listar_usuarios.html'
    success_url = reverse_lazy('gestao:usuarios')

    def get_success_url(self):
        return reverse_lazy('gestao:usuarios')


class ListarDocumentosEnteFederado(ListView):
    template_name = 'gestao/inserir_documentos/inserir_entefederado.html'
    paginate_by = 10

    def get_queryset(self):
        situacao = self.request.GET.get('situacao', None)
        ente_federado = self.request.GET.get('municipio', None)

        if situacao in ('1', '2', '3', '4', '5'):
            return Municipio.objects.filter(usuario__estado_processo=situacao)

        if ente_federado:
            municipio = Municipio.objects.filter(
                cidade__nome_municipio__icontains=ente_federado)
            estado = Municipio.objects.filter(
                cidade__nome_municipio__isnull=True,
                estado__nome_uf__icontains=ente_federado)

            return municipio | estado

        return Municipio.objects.filter(usuario__estado_processo__range=('1', '5'))


class AlterarDocumentosEnteFederado(UpdateView):

    template_name = 'gestao/inserir_documentos/alterar_entefederado.html'
    form_class = AlterarDocumentosEnteFederadoForm
    model = Municipio

    def get_success_url(self):
        return reverse_lazy('gestao:inserir_entefederado')


class InserirSistema(ListView):
    template_name = 'gestao/inserir_documentos/inserir_sistema.html'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', None)

        usuarios = Usuario.objects.filter(estado_processo='6')
        usuarios = usuarios.exclude(plano_trabalho__criacao_sistema=None)

        if q:
            usuarios = usuarios.filter(
                municipio__cidade__nome_municipio__icontains=q)

        return usuarios


class AlterarSistema(UpdateView):
    template_name = 'gestao/inserir_documentos/alterar_sistema.html'
    form_class = AlterarSistemaForm
    model = CriacaoSistema

    def get_success_url(self):
        return reverse_lazy('gestao:inserir_sistema')


class InserirOrgao(ListView):
    template_name = 'gestao/inserir_documentos/inserir_orgao.html'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        usuarios = Usuario.objects.filter(estado_processo='6')
        usuarios = usuarios.exclude(plano_trabalho__orgao_gestor=None)

        if q:
            usuarios = usuarios.filter(
                municipio__cidade__nome_municipio__icontains=q)
        return usuarios


class AlterarOrgao(UpdateView):
    template_name = 'gestao/inserir_documentos/alterar_orgao.html'
    form_class = AlterarOrgaoForm
    model = OrgaoGestor

    def get_success_url(self):
        return reverse_lazy('gestao:inserir_orgao')


class InserirConselho(ListView):
    template_name = 'gestao/inserir_documentos/inserir_conselho.html'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        usuarios = Usuario.objects.filter(estado_processo='6')
        usuarios = usuarios.exclude(plano_trabalho__conselho_cultural=None)

        if q:
            usuarios = usuarios.filter(
                municipio__cidade__nome_municipio__icontains=q)
        return usuarios


class AlterarConselho(UpdateView):
    template_name = 'gestao/inserir_documentos/alterar_conselho.html'
    form_class = AlterarConselhoForm
    model = ConselhoCultural

    def get_success_url(self):
        return reverse_lazy('gestao:inserir_conselho')


class InserirFundo(ListView):
    template_name = 'gestao/inserir_documentos/inserir_fundo.html'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        usuarios = Usuario.objects.filter(estado_processo='6')
        usuarios = usuarios.exclude(plano_trabalho__fundo_cultura=None)

        if q:
            usuarios = usuarios.filter(
                municipio__cidade__nome_municipio__icontains=q)
        return usuarios


class AlterarFundo(UpdateView):
    template_name = 'gestao/inserir_documentos/alterar_fundo.html'
    form_class = AlterarFundoForm
    model = FundoCultura

    def get_success_url(self):
        return reverse_lazy('gestao:inserir_fundo')


class InserirPlano(ListView):
    template_name = 'gestao/inserir_documentos/inserir_plano.html'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        usuarios = Usuario.objects.filter(estado_processo='6')
        usuarios = usuarios.exclude(plano_trabalho__plano_cultura=None)

        if q:
            usuarios = usuarios.filter(
                municipio__cidade__nome_municipio__icontains=q)

        return usuarios


class AlterarPlano(UpdateView):
    template_name = 'gestao/inserir_documentos/alterar_plano.html'
    form_class = AlterarPlanoForm
    model = PlanoCultura

    def get_success_url(self):
        return reverse_lazy('gestao:inserir_plano')


class Prorrogacao(ListView):
    template_name = 'gestao/prorrogacao/listar_prorrogacao.html'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        usuarios = Usuario.objects.filter(estado_processo='6')

        usuarios = usuarios.exclude(
            plano_trabalho__conselho_cultural=None,
            plano_trabalho__criacao_sistema=None,
            plano_trabalho__fundo_cultura=None,
            plano_trabalho__orgao_gestor=None,
            plano_trabalho__plano_cultura=None)

        if q:
            usuarios = usuarios.filter(
                municipio__cidade__nome_municipio__icontains=q)
        return usuarios


class ProrrogacaoFundo(UpdateView):
    template_name = 'gestao/prorrogacao/prorrogacao_fundo.html'
    form_class = ProrrogacaoFundoForm
    model = FundoCultura

    def get_success_url(self):
        return reverse_lazy('gestao:prorrogacao')


class ProrrogacaoConselho(UpdateView):
    template_name = 'gestao/prorrogacao/prorrogacao_conselho.html'
    form_class = ProrrogacaoConselhoForm
    model = ConselhoCultural

    def get_success_url(self):
        return reverse_lazy('gestao:prorrogacao')


class ProrrogacaoSistema(UpdateView):
    template_name = 'gestao/prorrogacao/prorrogacao_sistema.html'
    form_class = ProrrogacaoSistemaForm
    model = CriacaoSistema

    def get_success_url(self):
        return reverse_lazy('gestao:prorrogacao')


class ProrrogacaoOrgao(UpdateView):
    template_name = 'gestao/prorrogacao/prorrogacao_orgao.html'
    form_class = ProrrogacaoOrgaoForm
    model = OrgaoGestor

    def get_success_url(self):
        return reverse_lazy('gestao:prorrogacao')


class ProrrogacaoPlano(UpdateView):
    template_name = 'gestao/prorrogacao/prorrogacao_plano.html'
    form_class = ProrrogacaoPlanoForm
    model = PlanoCultura

    def get_success_url(self):
        return reverse_lazy('gestao:prorrogacao')
