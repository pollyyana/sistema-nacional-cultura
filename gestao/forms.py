from django.forms import ModelForm

from adesao.models import Usuario


class AlterarSituacao(ModelForm):
    class Meta:
        model = Usuario
        fields = ('estado_processo',)
