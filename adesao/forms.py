from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario
from .utils import validar_cpf


class CadastrarUsuarioForm(UserCreationForm):
    cpf = forms.CharField(max_length=14)
    confirmar_email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email')

    def clean_confirmar_email(self):
        if self.cleaned_data['email'] != self.cleaned_data['confirmar_email']:
            raise forms.ValidationError(
                'Confirmação de e-mail não confere.')

    def clean_cpf(self):
        if not validar_cpf(self.cleaned_data['cpf']):
            raise forms.ValidationError('Por favor, digite um CPF válido!')

        if User.objects.filter(username=self.cleaned_data['cpf']).count():
            raise forms.ValidationError('Esse CPF já foi cadastrado.')

        if not self.cleaned_data['cpf']:
            raise forms.ValidationError('Este campo é obrigatório.')

        return self.cleaned_data['cpf']
