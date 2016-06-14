from threading import Thread
from django import forms
from django.core.mail import send_mail
from django.forms import ModelForm
from django.contrib.auth.models import User

from adesao.models import Usuario, Historico, Uf, Municipio
from planotrabalho.models import PlanoTrabalho

from .utils import enviar_email_alteracao_situacao

from ckeditor.widgets import CKEditorWidget

from clever_selects.form_fields import ChainedChoiceField
from clever_selects.forms import ChainedChoicesForm


class AlterarSituacao(ModelForm):
    justificativa = forms.CharField(required=False)
    localizacao = forms.CharField(max_length="10", required=False)
    num_processo = forms.CharField(max_length="50", required=False)

    def save(self, commit=True):
        usuario = super(AlterarSituacao, self).save(commit=False)
        historico = Historico()
        historico.usuario = usuario
        historico.situacao = self.cleaned_data['estado_processo']

        if self.cleaned_data['estado_processo'] == '2':
            usuario.municipio.localizacao = self.cleaned_data['localizacao']
        elif self.cleaned_data['estado_processo'] == '3':
            historico.descricao = self.cleaned_data['justificativa']
        elif self.cleaned_data['estado_processo'] == '4':
            usuario.municipio.numero_processo = self.cleaned_data['num_processo']
        elif self.cleaned_data['estado_processo'] == '6':
            if usuario.plano_trabalho is None:
                plano_trabalho = PlanoTrabalho()

                if commit:
                    plano_trabalho.save()

                usuario.plano_trabalho = plano_trabalho
                print(usuario.plano_trabalho)

        if commit:
            usuario.municipio.save()
            usuario.save()
            historico.save()
            enviar_email_alteracao_situacao(usuario, historico)

    class Meta:
        model = Usuario
        fields = ('estado_processo', 'data_publicacao_acordo')


class DiligenciaForm(forms.Form):
    diligencia = forms.CharField(required=False, widget=CKEditorWidget())

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super(DiligenciaForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        subject = '[Sistema Nacional de Cultura] Diligência em anexo'
        Thread(target=send_mail, args=(
            subject,
            self.cleaned_data['diligencia'],
            'naoresponda@cultura.gov.br',
            [self.usuario.user.email],),
            kwargs = {
                'fail_silently': 'False',
                'html_message': self.cleaned_data['diligencia']}
            ).start()


class AlterarCadastradorForm(ChainedChoicesForm):
    cpf_usuario = forms.CharField(max_length=11)
    uf = forms.ModelChoiceField(queryset=Uf.objects.all())
    municipio = ChainedChoiceField(
        parent_field='uf',
        ajax_url='/gestao/chain/municipio',
        empty_label='-- Município --',
        required=False)
    data_publicacao_acordo = forms.DateField(required=False)

    def clean_cpf_usuario(self):
        cpf_usuario = self.cleaned_data['cpf_usuario']

        if not Usuario.objects.filter(user__username__iexact=cpf_usuario):
            raise forms.ValidationError('Cadastrador não encontrado, o usuário efetuou cadastro?')

        return cpf_usuario

    def clean_municipio(self):
        municipio = self.cleaned_data['municipio']
        if not municipio:
            municipio = None
        uf = self.cleaned_data['uf']
        if not Municipio.objects.filter(cidade=municipio, estado=uf):
            raise forms.ValidationError('Município não cadastrado')
        return municipio

    def clean(self):
        super(AlterarCadastradorForm, self).clean()
        cpf_usuario = self.cleaned_data.get('cpf_usuario', None)
        municipio = self.cleaned_data.get('municipio', None)
        uf = self.cleaned_data.get('uf', None)
        try:
            user_antigo = Usuario.objects.get(
                municipio__cidade=municipio, municipio__estado__sigla=uf)
            user_novo = Usuario.objects.get(user__username__iexact=cpf_usuario)

            if user_antigo.user.username == user_novo.user.username:
                raise forms.ValidationError('Cadastrador já se encontra vinculado ao municípío selecionado.')
            if not user_antigo.data_publicacao_acordo and not self.cleaned_data.get('data_publicacao_acordo', None):
                raise forms.ValidationError(
                    'Não foi encontrada a data de publicação do acordo deste município, por favor informe a data')
        except Usuario.DoesNotExist:
            if not self.cleaned_data.get('data_publicacao_acordo', None):
                raise forms.ValidationError(
                    'Não foi encontrada a data de publicação do acordo deste município, por favor informe a data')

    def save(self, commit=True):
        cpf_usuario = self.cleaned_data['cpf_usuario']
        municipio = self.cleaned_data.get('municipio', None)
        uf = self.cleaned_data['uf']
        data_publicacao_acordo = self.cleaned_data['data_publicacao_acordo']
        user_novo = Usuario.objects.get(user__username__iexact=cpf_usuario)
        try:
            if municipio:
                user_antigo = Usuario.objects.get(municipio__cidade=municipio, municipio__estado=uf)
            else:
                user_antigo = Usuario.objects.get(municipio__cidade__isnull=True, municipio__estado=uf)

            user_novo.municipio = user_antigo.municipio
            user_antigo.municipio = None

            user_novo.responsavel = user_antigo.responsavel
            user_antigo.responsavel = None

            user_novo.secretario = user_antigo.secretario
            user_antigo.secretario = None

            user_novo.plano_trabalho = user_antigo.plano_trabalho
            user_antigo.plano_trabalho = None

            user_antigo.user.is_active = False
            user_antigo.estado_processo = '0'
            user_novo.estado_processo = '6'

            user_novo.prazo = user_antigo.prazo

            if data_publicacao_acordo:
                user_novo.data_publicacao_acordo = data_publicacao_acordo
            else:
                user_novo.data_publicacao_acordo = user_antigo.data_publicacao_acordo
        except Usuario.DoesNotExist:
            if municipio:
                user_antigo = Municipio.objects.get(cidade=municipio, estado=uf)
            else:
                user_antigo = Municipio.objects.get(cidade__isnull=True, estado=uf)
            planotrabalho = PlanoTrabalho()
            planotrabalho.save()

            user_novo.municipio = user_antigo
            user_novo.data_publicacao_acordo = data_publicacao_acordo
            user_novo.estado_processo = '6'
            user_novo.plano_trabalho = planotrabalho

        if commit:
            user_antigo.save()
            user_novo.save()


class AlterarUsuarioForm(ModelForm):
    is_active = forms.BooleanField()
    is_staff = forms.BooleanField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('is_active', 'is_staff', 'email')
