from django import forms
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.forms import ModelForm
from django.template.defaultfilters import filesizeformat
from django.core.urlresolvers import reverse

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


class CadastrarUsuarioForm(UserCreationForm):
    username = forms.CharField(max_length=14, required=True)
    confirmar_email = forms.EmailField(required=True)
    email = forms.EmailField(required=True)
    nome_usuario = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_confirmar_email(self):
        if self.data.get('email') != self.cleaned_data['confirmar_email']:
            raise forms.ValidationError(
                'Confirmação de e-mail não confere.')

        return self.cleaned_data['confirmar_email']

    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
            raise forms.ValidationError('Este e-mail já foi cadastrado!')
        except User.DoesNotExist:
            return self.cleaned_data['email']

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
        user.email = self.cleaned_data['email']
        user.is_active = False
        if commit:
            user.save()

        usuario = Usuario()
        usuario.user = user
        usuario.nome_usuario = self.cleaned_data['nome_usuario']
        codigo_ativacao = get_random_string()
        usuario.codigo_ativacao = codigo_ativacao
        if commit:
            usuario.save()
        Thread(target=send_mail, args=(
            'MINISTÉRIO DA CULTURA - SNC - CREDENCIAIS DE ACESSO',
            'Prezado '+usuario.nome_usuario+',\n' +
            'Recebemos o seu cadastro no Sistema Nacional de Cultura.' +
            'Por favor confirme seu e-mail clicando no endereço abaixo:\n\n' +
            reverse('adesao:ativar_usuario', args=[codigo_ativacao])+'\n\n' +
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
        if not validar_cpf(self.cleaned_data['cpf_prefeito']):
            raise forms.ValidationError('Por favor, digite um CPF válido!')

        return self.cleaned_data['cpf_prefeito']

    def clean_cnpj_prefeitura(self):
        if not validar_cnpj(self.cleaned_data['cnpj_prefeitura']):
            raise forms.ValidationError('Por favor, digite um CNPJ válido!')

        return self.cleaned_data['cnpj_prefeitura']

    class Meta:
        model = Municipio
        fields = '__all__'


class CadastrarSecretarioForm(ModelForm):
    def clean_cpf_secretario(self):
        if not validar_cpf(self.cleaned_data['cpf_secretario']):
            raise forms.ValidationError('Por favor, digite um CPF válido!')

        return self.cleaned_data['cpf_secretario']

    class Meta:
        model = Secretario
        fields = '__all__'


class CadastrarResponsavelForm(ModelForm):
    def clean_cpf_responsavel(self):
        if not validar_cpf(self.cleaned_data['cpf_responsavel']):
            raise forms.ValidationError('Por favor, digite um CPF válido!')

        return self.cleaned_data['cpf_responsavel']

    class Meta:
        model = Responsavel
        fields = '__all__'
