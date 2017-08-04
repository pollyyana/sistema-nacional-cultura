from django.shortcuts import redirect, render
from django.http import Http404, JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, UpdateView

from adesao.models import Usuario, Cidade, Municipio, Historico
from planotrabalho.models import CriacaoSistema, PlanoCultura, FundoCultura, OrgaoGestor, ConselhoCultural
from gestao.utils import enviar_email_aprovacao_plano

from .forms import AlterarSituacao, DiligenciaForm, AlterarDocumentosEnteFederadoForm
from .forms import AlterarCadastradorForm, AlterarUsuarioForm, AlterarOrgaoForm
from .forms import AlterarFundoForm, AlterarPlanoForm, AlterarConselhoForm, AlterarSistemaForm

from clever_selects.views import ChainedSelectChoicesView

import os
from django.conf import settings


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

            # try:
            #     usuario = Usuario.objects.get(
            #         id=id, plano_trabalho__criacao_sistema__situacao_lei_sistema_id='2',
            #         plano_trabalho__conselho_cultural__situacao_ata_id='2',
            #         plano_trabalho__fundo_cultura__situacao_lei_plano_id='2',
            #         plano_trabalho__orgao_gestor__situacao_relatorio_secretaria_id='2',
            #         plano_trabalho__plano_cultura__situacao_lei_plano_id='2')
            #     usuario = User.objects.get(id=usuario.user_id)
            #
            #     message_txt = render('emails/aprovacao_plano.txt')
            #     message_html = render('emails/aprovacao_plano.email')
            #     enviar_email_aprovacao_plano(usuario, message_txt, message_html)
            # except Exception as e:
            #     return redirect('gestao:detalhar', pk=id)

    return redirect('gestao:detalhar', pk=id)


def ajax_cadastrador_cpf(request):
    if request.method == "POST":
        try:
            ente_federado = request.POST.get("ente_federado", None)
            estado = request.POST.get("estado", None)

            if estado:
                municipio = Municipio.objects.get(cidade__isnull=True, estado_id=ente_federado)
            else:
                municipio = Municipio.objects.get(cidade=ente_federado)

            usuario = Usuario.objects.get(municipio_id=municipio.id)
            user = User.objects.get(id=usuario.user_id)
            if usuario.data_publicacao_acordo:
                data_de_publicacao = usuario.data_publicacao_acordo.strftime('%d/%m/%Y')
            else:
                data_de_publicacao = None

            data = {
                'cpf': user.username,
                'data_publicacao_acordo': data_de_publicacao,
                'estado_processo': usuario.estado_processo
                }
            return JsonResponse(data)

        except:
            return JsonResponse(data={"erro": True})
    else:
        return JsonResponse(data={"erro": True})


class AcompanharPrazo(ListView):
    template_name = 'gestao/acompanhar_prazo.html'
    paginate_by = 10

    def get_queryset(self):
        ente_federado = self.request.GET.get('municipio', None)
        if ente_federado:
            municipio = Usuario.objects.filter(
                municipio__cidade__nome_municipio__icontains=ente_federado).order_by('municipio__estado__nome_uf')
            estado = Usuario.objects.filter(
                municipio__cidade__isnull=True,
                municipio__estado__nome_uf__icontains=ente_federado).order_by('municipio__estado__nome_uf')

            return municipio | estado
        return Usuario.objects.filter(estado_processo='6', data_publicacao_acordo__isnull=False).order_by(
            'municipio__estado__nome_uf')


def aditivar_prazo(request, id):
    if request.method == "POST":
        user = Usuario.objects.get(id=id)
        user.prazo = user.prazo + 1
        user.save()

    return redirect('gestao:acompanhar_prazo')


class AcompanharAdesao(ListView):
    template_name = 'gestao/adesao/acompanhar.html'
    paginate_by = 10

    def get_queryset(self):
        situacao = self.request.GET.get('situacao', None)
        ente_federado = self.request.GET.get('municipio', None)

        if situacao in ('1', '2', '3', '4', '5', '6'):
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
    return redirect('gestao:detalhar', pk=id)

def situacao_3 (request, etapa, st, id):
    usuario = Usuario.objects.get(id=id)
    setattr(getattr(usuario.plano_trabalho, etapa), st, 3)
    getattr(usuario.plano_trabalho, etapa).save()
    return redirect('gestao:detalhar', pk=id)

def situacao_4 (request, etapa, st, id):
    usuario = Usuario.objects.get(id=id)
    setattr(getattr(usuario.plano_trabalho, etapa), st, 4)
    getattr(usuario.plano_trabalho, etapa).save()
    return redirect('gestao:detalhar', pk=id)

def situacao_5 (request, etapa, st, id):
    usuario = Usuario.objects.get(id=id)
    setattr(getattr(usuario.plano_trabalho, etapa), st, 5)
    getattr(usuario.plano_trabalho, etapa).save()
    return redirect('gestao:detalhar', pk=id)

def situacao_6 (request, etapa, st, id):
    usuario = Usuario.objects.get(id=id)
    setattr(getattr(usuario.plano_trabalho, etapa), st, 6)
    getattr(usuario.plano_trabalho, etapa).save()
    return redirect('gestao:detalhar', pk=id)




class DetalharUsuario(DetailView):
    model = Usuario
    template_name = 'gestao/detalhe_municipio.html'

    def get_context_data(self, **kwargs):
        context = super(DetalharUsuario, self).get_context_data(**kwargs)
        situacao = context['usuario'].estado_processo
        try:

            if situacao == '3':
                historico = Historico.objects.filter(usuario_id=context['usuario'].id)
                historico = historico[0]
                context['dado_situacao'] = historico.descricao

            elif situacao == '2':
                municipio = Municipio.objects.get(usuario__id=context['usuario'].id)
                context['dado_situacao'] = municipio.localizacao

            elif situacao == '4':
                municipio = Municipio.objects.get(usuario__id=context['usuario'].id)
                context['dado_situacao'] = municipio.numero_processo

            elif situacao == '6':
                context['dado_situacao'] = context['usuario'].data_publicacao_acordo.strftime('%d/%m/%Y')
        except:
            pass
        return context


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
