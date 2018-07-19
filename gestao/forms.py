from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.template.defaultfilters import filesizeformat

from dal import autocomplete

from ckeditor.widgets import CKEditorWidget

from adesao.models import Usuario
from adesao.models import Historico
from adesao.models import Cidade
from adesao.models import Uf
from adesao.models import Municipio
from adesao.models import LISTA_ESTADOS_PROCESSO

from planotrabalho.models import CriacaoSistema, FundoCultura
from planotrabalho.models import PlanoCultura, OrgaoGestor, ConselhoCultural
from planotrabalho.models import SituacoesArquivoPlano

from gestao.models import Diligencia

from .utils import enviar_email_alteracao_situacao


content_types = [
    'image/png',
    'image/jpg',
    'image/jpeg',
    'application/pdf',
    'application/msword',
    'application/vnd.oasis.opendocument.text',
    'application/vnd.openxmlformats-officedocument.' +
    'wordprocessingml.document',
    'application/x-rar-compressed',
    'application/zip',
    'application/octet-stream',
    'text/plain']

max_upload_size = 5242880


class RestrictedFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")
        self.max_upload_size = kwargs.pop("max_upload_size")

        super(RestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        file = super(RestrictedFileField, self).clean(data, initial)

        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError(
                        'O arquivo deve ter menos de %s. Tamanho atual %s'
                        % (filesizeformat(self.max_upload_size),
                            filesizeformat(file._size)))
            else:
                raise forms.ValidationError(
                    'Arquivos desse tipo não são aceitos.')
        except AttributeError:
            pass

        return data


class AlterarDadosAdesao(ModelForm):
    processo_sei = forms.CharField(max_length="50", required=False)
    justificativa = forms.CharField(required=False)
    localizacao = forms.CharField(max_length="10", required=False)
    num_processo = forms.CharField(max_length="50", required=False)
    estado_processo = forms.ChoiceField(choices=LISTA_ESTADOS_PROCESSO, required=False)

    def clean(self):
        if self.cleaned_data.get('estado_processo', None) == '6':
            if not self.cleaned_data.get('data_publicacao_acordo', None):
                raise forms.ValidationError('Insira a data corretamente.')

    def save(self, commit=True):
        usuario = super(AlterarDadosAdesao, self).save(commit=False)
        historico = Historico()
        historico.usuario = usuario
        historico.situacao = self.cleaned_data['estado_processo']

        if self.cleaned_data['estado_processo'] == '2':
            usuario.municipio.localizacao = self.cleaned_data['localizacao']
        elif self.cleaned_data['estado_processo'] == '3':
            historico.descricao = self.cleaned_data['justificativa']
        elif self.cleaned_data['estado_processo'] == '4':
            usuario.municipio.numero_processo = self.cleaned_data['num_processo']

        if commit:
            usuario.municipio.save()
            usuario.save()
            historico.save()
            enviar_email_alteracao_situacao(usuario, historico)

    class Meta:
        model = Usuario
        fields = ('estado_processo', 'data_publicacao_acordo', 'link_publicacao_acordo',
                  'processo_sei')


class DiligenciaForm(ModelForm):
    texto_diligencia = forms.CharField(widget=CKEditorWidget())

    def __init__(self, resultado, componente, *args, **kwargs):
        """ Form da diligência recebe como parâmetro o resultado, que serve
        para diferenciar diligência de aprovação e reprovação """

        super(DiligenciaForm, self).__init__(*args, **kwargs)

        if componente != 'plano_trabalho':
            if resultado == '1':
                self.fields['classificacao_arquivo'].queryset = SituacoesArquivoPlano.objects.filter(pk=2)
            else:
                self.fields['classificacao_arquivo'].queryset = SituacoesArquivoPlano.objects.filter(id__gte=4, id__lte=6)
        else:
            self.fields.pop('classificacao_arquivo')

    class Meta:
        model = Diligencia
        fields = ('texto_diligencia', 'classificacao_arquivo')


class AlterarCadastradorForm(forms.Form):
    cpf_usuario = forms.CharField(max_length=11)
    estado = forms.ModelChoiceField(queryset=Uf.objects.all(),
                                    widget=autocomplete.ModelSelect2(url='gestao:uf_chain'))
    municipio = forms.ModelChoiceField(
        queryset=Cidade.objects.all(),
        widget=autocomplete.ModelSelect2(url='gestao:cidade_chain',
                                         forward=['estado'])
        )
    data_publicacao_acordo = forms.DateField(required=False)

    class Meta:
        fields = ('cpf_usuario', 'estado', 'municipio', 'data_publicacao_acordo')
    # municipio = ChainedChoiceField(
#         parent_field='uf',
#         ajax_url='/gestao/chain/municipio',
#         empty_label='-- Município --',
#         required=False)

#     def clean_cpf_usuario(self):
#         cpf_usuario = self.cleaned_data['cpf_usuario']

#         if not Usuario.objects.filter(user__username__iexact=cpf_usuario):
#             raise forms.ValidationError('Cadastrador não encontrado, o usuário efetuou cadastro?')

#         return cpf_usuario

#     def clean_municipio(self):
#         municipio = self.cleaned_data['municipio']
#         if not municipio:
#             municipio = None
#         uf = self.cleaned_data['uf']
#         if not Municipio.objects.filter(cidade=municipio, estado=uf):
#             raise forms.ValidationError('Município não cadastrado')
#         return municipio

#     def clean(self):
#         super(AlterarCadastradorForm, self).clean()
#         cpf_usuario = self.cleaned_data.get('cpf_usuario', None)
#         municipio = self.cleaned_data.get('municipio', None)
#         uf = self.cleaned_data.get('uf', None)
#         try:
#             user_antigo = Usuario.objects.get(
#                 municipio__cidade=municipio, municipio__estado__sigla=uf)
#             user_novo = Usuario.objects.get(user__username__iexact=cpf_usuario)

#             if user_antigo.user.username == user_novo.user.username:
#                 raise forms.ValidationError('Cadastrador já se encontra vinculado ao municípío selecionado.')
#             if user_antigo.estado_processo == '6':
#                 if not user_antigo.data_publicacao_acordo or not self.cleaned_data.get('data_publicacao_acordo', None):
#                     errormsg = '''Não foi encontrada a data de publicação
#                         do acordo deste município, por favor informe a data'''
#                     municipio = Municipio.objects.get(cidade=municipio, estado__sigla=uf)
#                     if municipio.numero_processo:
#                         errormsg += '. Ela pode ser encontrada no processo de número: ' + municipio.numero_processo
#                     raise forms.ValidationError(errormsg)
#         except:
#                 user_antigo = None
#                 pass

#     def save(self, commit=True):
#         cpf_usuario = self.cleaned_data['cpf_usuario']
#         municipio = self.cleaned_data.get('municipio', None)
#         uf = self.cleaned_data['uf']
#         data_publicacao_acordo = self.cleaned_data['data_publicacao_acordo']
#         user_novo = Usuario.objects.get(user__username__iexact=cpf_usuario)
#         try:
#             if municipio:
#                 user_antigo = Usuario.objects.get(municipio__cidade=municipio, municipio__estado=uf)
#             else:
#                 user_antigo = Usuario.objects.get(municipio__cidade__isnull=True, municipio__estado=uf)

#             user_novo.municipio = user_antigo.municipio
#             user_antigo.municipio = None

#             user_novo.responsavel = user_antigo.responsavel
#             user_antigo.responsavel = None

#             user_novo.secretario = user_antigo.secretario
#             user_antigo.secretario = None

#             user_novo.plano_trabalho = user_antigo.plano_trabalho
#             user_antigo.plano_trabalho = None

#             user_antigo.user.is_active = False
#             user_novo.estado_processo = user_antigo.estado_processo
#             user_antigo.estado_processo = '0'

#             user_novo.prazo = user_antigo.prazo

#             if data_publicacao_acordo:
#                 user_novo.data_publicacao_acordo = data_publicacao_acordo
#             else:
#                 user_novo.data_publicacao_acordo = user_antigo.data_publicacao_acordo
#         except Usuario.DoesNotExist:
#             if municipio:
#                 user_antigo = Municipio.objects.get(cidade=municipio, estado=uf)
#             else:
#                 user_antigo = Municipio.objects.get(cidade__isnull=True, estado=uf)
#             planotrabalho = PlanoTrabalho()
#             planotrabalho.save()

#             user_novo.municipio = user_antigo
#             user_novo.data_publicacao_acordo = data_publicacao_acordo
#             user_novo.estado_processo = '0'
#             user_novo.plano_trabalho = planotrabalho

#         if commit:
#             user_antigo.save()
#             user_novo.save()


class AlterarUsuarioForm(ModelForm):
    is_active = forms.BooleanField(required=False)
    is_staff = forms.BooleanField(required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ('is_active', 'is_staff', 'email')


class AlterarDocumentosEnteFederadoForm(ModelForm):
    termo_posse_prefeito = RestrictedFileField(
        content_types=content_types,
        max_upload_size=max_upload_size)
    rg_copia_prefeito = RestrictedFileField(
        content_types=content_types,
        max_upload_size=max_upload_size)
    cpf_copia_prefeito = RestrictedFileField(
        content_types=content_types,
        max_upload_size=max_upload_size)

    class Meta:
        model = Municipio
        fields = ('termo_posse_prefeito', 'rg_copia_prefeito', 'cpf_copia_prefeito')


class AlterarSistemaForm(ModelForm):
    arquivo = RestrictedFileField(
        content_types=content_types,
        max_upload_size=max_upload_size)

    class Meta:
        model = CriacaoSistema
        fields = ('arquivo',)


class AlterarFundoForm(ModelForm):
    arquivo = RestrictedFileField(
        content_types=content_types,
        max_upload_size=max_upload_size)

    class Meta:
        model = FundoCultura
        fields = ('arquivo',)


class AlterarPlanoForm(ModelForm):
    arquivo = RestrictedFileField(
        content_types=content_types,
        max_upload_size=max_upload_size)

    class Meta:
        model = PlanoCultura
        fields = ('arquivo',)


class AlterarOrgaoForm(ModelForm):
    arquivo = RestrictedFileField(
        content_types=content_types,
        max_upload_size=max_upload_size)

    class Meta:
        model = OrgaoGestor
        fields = ('arquivo',)


class AlterarConselhoForm(ModelForm):
    arquivo = RestrictedFileField(
        content_types=content_types,
        max_upload_size=max_upload_size)

    class Meta:
        model = ConselhoCultural
        fields = ('arquivo',)
