from datetime import timedelta

from django import forms
from django.forms import ModelForm

from .models import CriacaoSistema, OrgaoGestor, ConselhoCultural
from .models import FundoCultura, PlanoCultura
from adesao.models import Usuario
from .utils import get_or_none


class CriarSistemaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('user')
        super(CriarSistemaForm, self).__init__(*args, **kwargs)

    def clean_data_final_elaboracao_projeto_lei(self):
        data_limite = self.usuario.data_publicacao_acordo + timedelta(days=2*365)
        if self.cleaned_data['data_final_elaboracao_projeto_lei']  > (data_limite):
            raise forms.ValidationError('A data deve ser anterior a ' +str(data_limite))

        return self.cleaned_data['data_final_elaboracao_projeto_lei']

    def clean_data_final_sancao_lei(self):
        data_limite = self.usuario.data_publicacao_acordo + timedelta(days=2*365)
        if self.cleaned_data['data_final_sancao_lei'] > (data_limite):
            raise forms.ValidationError('A data deve ser anterior a '+str(data_limite))
        return self.cleaned_data['data_final_sancao_lei']

    class Meta:
        model = CriacaoSistema
        fields = '__all__'


class OrgaoGestorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('user')
        super(OrgaoGestorForm, self).__init__(*args, **kwargs)

    def clean_data_final_estruturacao_secretaria(self):
        data_limite = self.usuario.data_publicacao_acordo + timedelta(days=2*365)
        if self.cleaned_data['data_final_estruturacao_secretaria']  > (data_limite):
            raise forms.ValidationError('A data deve ser anterior a ' +str(data_limite))

        return self.cleaned_data['data_final_estruturacao_secretaria']

    class Meta:
        model = OrgaoGestor
        fields = '__all__'


class ConselhoCulturalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('user')
        super(ConselhoCulturalForm, self).__init__(*args, **kwargs)

    def clean_data_final_instalacao_conselho(self):
        data_limite = self.usuario.data_publicacao_acordo + timedelta(days=2*365)
        if self.cleaned_data['data_final_instalacao_conselho']  > (data_limite):
            raise forms.ValidationError('A data deve ser anterior a ' +str(data_limite))

        return self.cleaned_data['data_final_instalacao_conselho']

    class Meta:
        model = ConselhoCultural
        fields = '__all__'


class FundoCulturaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('user')
        super(FundoCulturaForm, self).__init__(*args, **kwargs)

    def clean_data_final_instituicao_fundo_cultura(self):
        data_limite = self.usuario.data_publicacao_acordo + timedelta(days=2*365)
        if self.cleaned_data['data_final_instituicao_fundo_cultura']  > (data_limite):
            raise forms.ValidationError('A data deve ser anterior a ' +str(data_limite))

        return self.cleaned_data['data_final_instituicao_fundo_cultura']

    class Meta:
        model = FundoCultura
        fields = '__all__'


class PlanoCulturaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('user')
        super(PlanoCulturaForm, self).__init__(*args, **kwargs)

    def clean_data_final_estabelecimento_instancias(self):
        data_limite = self.usuario.data_publicacao_acordo + timedelta(days=2*365)
        if self.cleaned_data['data_final_estabelecimento_instancias']  > (data_limite):
            raise forms.ValidationError('A data deve ser anterior a ' +str(data_limite))

        return self.cleaned_data['data_final_estabelecimento_instancias']

    def clean_data_final_elaboracao_plano_cultura(self):
        data_limite = self.usuario.data_publicacao_acordo + timedelta(days=2*365)
        if self.cleaned_data['data_final_elaboracao_plano_cultura']  > (data_limite):
            raise forms.ValidationError('A data deve ser anterior a ' +str(data_limite))

        return self.cleaned_data['data_final_elaboracao_plano_cultura']

    def clean_data_final_aprovacao_plano_cultura(self):
        data_limite = self.usuario.data_publicacao_acordo + timedelta(days=2*365)
        if self.cleaned_data['data_final_aprovacao_plano_cultura']  > (data_limite):
            raise forms.ValidationError('A data deve ser anterior a ' +str(data_limite))

        return self.cleaned_data['data_final_aprovacao_plano_cultura']

    def clean_data_final_tramitacao_projeto_lei(self):
        data_limite = self.usuario.data_publicacao_acordo + timedelta(days=2*365)
        if self.cleaned_data['data_final_tramitacao_projeto_lei']  > (data_limite):
            raise forms.ValidationError('A data deve ser anterior a ' +str(data_limite))

        return self.cleaned_data['data_final_tramitacao_projeto_lei']

    def clean_data_final_sancao_lei_plano_cultura(self):
        data_limite = self.usuario.data_publicacao_acordo + timedelta(days=2*365)
        if self.cleaned_data['data_final_sancao_lei_plano_cultura'] > data_limite:
            raise forms.ValidationError('A data deve ser anterior a ' +str(data_limite))

        return self.cleaned_data['data_final_sancao_lei_plano_cultura']

    class Meta:
        model = PlanoCultura
        fields = '__all__'
