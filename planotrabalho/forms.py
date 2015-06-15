from datetime import timedelta

from django import forms
from django.forms import ModelForm

from .models import CriacaoSistema, OrgaoGestor, ConselhoCultural
from .models import FundoCultura, PlanoCultura
from adesao.models import Usuario
from .utils import get_or_none


class CriarSistemaForm(ModelForm):
    def __init__(self, **kwargs):
        user = kwargs.pop('user')
        super(CriarSistemaForm, self).__init__(**kwargs)
        self.usuario = Usuario.objects.get(user=user)

    def clean_data_final_elaboracao_projeto_lei(self):
        data_limite = self.usuario.data_publicacao_acordo + timedelta(days=2*365)
        if self.cleaned_data['data_final_elaboracao_projeto_lei']  > (data_limite):
            raise forms.ValidationError('A data deve ser inferior a ' +(data_limite))

        return self.cleaned_data['data_final_elaboracao_projeto_lei']

    def clean_data_final_sancao_lei(self):
        data_limite = self.usuario.data_publicacao_acordo + timedelta(days=2*365)
        if self.cleaned_data['data_final_sancao_lei'] > (data_limite):
            raise forms.ValidationError('A data deve ser inferior a '+(data_limite))
        return self.cleaned_data['data_final_sancao_lei']

    class Meta:
        model = CriacaoSistema
        fields = '__all__'


class OrgaoGestorForm(ModelForm):
    class Meta:
        model = OrgaoGestor
        fields = '__all__'


class ConselhoCulturalForm(ModelForm):
    class Meta:
        model = ConselhoCultural
        fields = '__all__'


class FundoCulturaForm(ModelForm):
    class Meta:
        model = FundoCultura
        fields = '__all__'


class PlanoCulturaForm(ModelForm):
    class Meta:
        model = PlanoCultura
        fields = '__all__'
