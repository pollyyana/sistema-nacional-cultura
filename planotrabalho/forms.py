from datetime import timedelta

from django import forms
from django.forms import ModelForm

from .models import CriacaoSistema, OrgaoGestor, ConselhoCultural
from .models import FundoCultura, PlanoCultura
from adesao.models import Usuario


class CriarSistemaForm(ModelForm):
    def __init__(self, *args, request=None, **kwargs):
        self.usuario = Usuario.objects.get(user=self.request.user)
        self.data_publicacao = self.usuario.data_publicacao_acordo
        return super(CriarSistemaForm,self).__init__(self,*args,**kwargs)
      
    def clean_data_final_elaboracao_projeto_lei(self):
        data_limite = self.data_publicacao + timedelta(years=2)
        if self.cleaned_data['data_final_elaboracao_projeto_lei']  > (data_limite):
            raise forms.ValidationError('A data deve ser inferior a ' +(data_limite))
        
        return self.cleaned_data['data_final_elaboracao_projeto_lei']
    
    def clean_data_final_sancao_lei(self):
        data_limite = self.data_publicacao + timedelta(years=2)
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
