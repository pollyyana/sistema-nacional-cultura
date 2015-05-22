from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.forms import ModelForm
from django.template.defaultfilters import filesizeformat

from threading import Thread

from .models import Usuario, Municipio, Responsavel, Secretario
from .utils import validar_cpf, validar_cnpj, limpar_mascara
import re

content_types = [
    'image/png',
    'application/pdf',
    'application/msword',
    'application/vnd.oasis.opendocument.text',
    'application/vnd.openxmlformats-officedocument.' +
    'wordprocessingml.document',
    'text/plain']


class RestrictedFileField(forms.FileField):
    """
    Same as FileField, but you can specify:
    * content_types - list containing allowed content_types.
    Example: ['application/pdf', 'image/jpeg']
    * max_upload_size - tamanho máximo para upload
        2.5MB - 2621440
        5MB - 5242880
        10MB - 10485760
        20MB - 20971520
        50MB - 5242880
        100MB - 104857600
        250MB - 214958080
        500MB - 429916160
"""

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
                raise forms.ValidationError('Tipo do arquivo não aceito.')
        except AttributeError:
            pass

        return data


class CadastrarUsuarioForm(UserCreationForm):
    username = forms.CharField(max_length=14, required=True)
    email = forms.EmailField(required=True)
    confirmar_email = forms.EmailField(required=True)
    nome_usuario = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('email', 'username')

    def __init__(self, *args, **kwargs):
        super(CadastrarUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def clean_confirmar_email(self):
        if self.cleaned_data['email'] != self.cleaned_data['confirmar_email']:
            raise forms.ValidationError(
                'Confirmação de e-mail não confere.')

        return self.cleaned_data['confirmar_email']

    def clean_username(self):
        if not validar_cpf(self.cleaned_data['username']):
            raise forms.ValidationError('Por favor, digite um CPF válido!')

        try:
            User.objects.get(username=''.join(re.findall(
                '\d+',
                self.cleaned_data['username'])))
            raise forms.ValidationError('Esse CPF já foi cadastrado.')
        except User.DoesNotExist:
            return self.cleaned_data['username']

        return self.cleaned_data['username']

    def save(self, commit=True):
        user = super(CadastrarUsuarioForm, self).save(commit=False)
        user.username = limpar_mascara(self.cleaned_data['username'])
        random_password = get_random_string(length=8)
        user.set_password(random_password)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        usuario = Usuario()
        usuario.user = user
        usuario.nome_usuario = self.cleaned_data['nome_usuario']
        if commit:
            usuario.save()
        print(user.email)
        Thread(target=send_mail, args=(
            'MINISTÉRIO DA CULTURA - SNC - CREDENCIAIS DE ACESSO',
            'Prezado '+usuario.nome_usuario+',\n' +
            'Recebemos o seu cadastro no Sistema Nacional de Cultura.' +
            'Seguem abaixo suas credenciais de acesso:\n\n' +
            'Login: '+user.username+'\n' +
            'Senha: '+random_password+'\n\n' +
            'Atenciosamente,\n\n' +
            'Equipe SAI - Ministério da Cultura',
            '',
            [user.email],),
            kwargs = {'fail_silently': 'False', }
        ).start()
        return user


class CadastrarMunicipioForm(ModelForm):
    termo_posse_prefeito = RestrictedFileField(
        content_types=content_types,
        max_upload_size=5242880)
    rg_copia_prefeito = RestrictedFileField(
        content_types=content_types,
        max_upload_size=5242880)
    cpf_copia_prefeito = RestrictedFileField(
        content_types=content_types,
        max_upload_size=5242880)

    def clean_cpf_prefeito(self):
        cpf_prefeito = limpar_mascara(self.cleaned_data['cpf_prefeito'])
        if not validar_cpf(cpf_prefeito):
            raise forms.ValidationError('Por favor, digite um CPF válido!')

        return cpf_prefeito

    def clean_cnpj_prefeitura(self):
        cnpj_prefeitura = limpar_mascara(self.cleaned_data['cnpj_prefeitura'])
        if not validar_cnpj(cnpj_prefeitura):
            raise forms.ValidationError('Por favor, digite um CNPJ válido!')

        return cnpj_prefeitura

    class Meta:
        model = Municipio
        fields = '__all__'


class CadastrarSecretarioForm(ModelForm):
    def clean_cpf_secretario(self):
        cpf_secretario = limpar_mascara(self.cleaned_data['cpf_secretario'])
        if not validar_cpf(cpf_secretario):
            raise forms.ValidationError('Por favor, digite um CPF válido!')

        return cpf_secretario

    class Meta:
        model = Secretario
        fields = '__all__'


class CadastrarResponsavelForm(ModelForm):
    def clean_cpf_responsavel(self):
        cpf_responsavel = limpar_mascara(self.cleaned_data['cpf_responsavel'])
        if not validar_cpf(cpf_responsavel):
            raise forms.ValidationError('Por favor, digite um CPF válido!')

        return cpf_responsavel

    class Meta:
        model = Responsavel
        fields = '__all__'
