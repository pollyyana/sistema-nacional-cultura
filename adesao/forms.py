from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.forms import ModelForm

from thread import start_new_thread

from .models import Usuario, Municipio, Responsavel, Secretario
from .utils import validar_cpf, validar_cnpj
import re


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
        user.username = ''.join(re.findall(
            '\d+',
            self.cleaned_data['username']))
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

        start_new_thread(send_mail(
            'MINISTÉRIO DA CULTURA - SNC - CREDENCIAIS DE ACESSO',
            'Prezado '+usuario.nome_usuario+',\n' +
            'Recebemos o seu cadastro no Sistema Nacional de Cultura.' +
            'Seguem abaixo suas credenciais de acesso:\n\n' +
            'Login: '+user.username+'\n' +
            'Senha: '+random_password+'\n\n' +
            'Atenciosamente,\n\n' +
            'Equipe SAI - Ministério da Cultura',
            'snc@cultura.gov.br',
            [user.email],
            fail_silently=False
        ))
        return user


class CadastrarMunicipio(ModelForm):
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


class CadastrarSecretario(ModelForm):
    def clean_cpf_secretario(self):
        if not validar_cpf(self.cleaned_data['cpf_secretario']):
            raise forms.ValidationError('Por favor, digite um CPF válido!')

        return self.cleaned_data['cpf_secretario']

    class Meta:
        model = Secretario
        fields = '__all__'


class CadastrarResponsavel(ModelForm):
    def clean_cpf_secretario(self):
        if not validar_cpf(self.cleaned_data['cpf_responsavel']):
            raise forms.ValidationError('Por favor, digite um CPF válido!')

        return self.cleaned_data['cpf_responsavel']

    class Meta:
        model = Responsavel
        fields = '__all__'
