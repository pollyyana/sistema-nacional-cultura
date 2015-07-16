from datetime import timedelta

from django import forms
from django.forms import ModelForm

from .models import CriacaoSistema, OrgaoGestor, ConselhoCultural
from .models import FundoCultura, PlanoCultura


class CriarSistemaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('user')
        super(CriarSistemaForm, self).__init__(*args, **kwargs)

    def clean_data_final_elaboracao_projeto_lei(self):
        limite = self.usuario.data_publicacao_acordo
        +timedelta(days=2 * 365)

        if self.cleaned_data['data_final_elaboracao_projeto_lei'] > limite:
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        str(limite))

        return self.cleaned_data['data_final_elaboracao_projeto_lei']

    def clean_data_final_sancao_lei(self):
        limite = self.usuario.data_publicacao_acordo
        +timedelta(days=2 * 365)

        if self.cleaned_data['data_final_sancao_lei'] > (limite):
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        str(limite))

        return self.cleaned_data['data_final_sancao_lei']

    class Meta:
        model = CriacaoSistema
        exclude = ['situacao_minuta', 'situacao_lei_sistema']


class OrgaoGestorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('user')
        super(OrgaoGestorForm, self).__init__(*args, **kwargs)

    def clean_data_final_estruturacao_secretaria(self):
        limite = self.usuario.data_publicacao_acordo
        +timedelta(days=2 * 365)

        if self.cleaned_data['data_final_estruturacao_secretaria'] > limite:
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        str(limite))

        return self.cleaned_data['data_final_estruturacao_secretaria']

    class Meta:
        model = OrgaoGestor
        exclude = ['situacao_relatorio_secretaria']


class ConselhoCulturalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('user')
        super(ConselhoCulturalForm, self).__init__(*args, **kwargs)

    def clean_data_final_instalacao_conselho(self):
        limite = self.usuario.data_publicacao_acordo
        +timedelta(days=2 * 365)

        if self.cleaned_data['data_final_instalacao_conselho'] > limite:
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        str(limite))

        return self.cleaned_data['data_final_instalacao_conselho']

    class Meta:
        model = ConselhoCultural
        exclude = ['situacao_ata']


class FundoCulturaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('user')
        super(FundoCulturaForm, self).__init__(*args, **kwargs)

    def clean_data_final_instituicao_fundo_cultura(self):
        limite = self.usuario.data_publicacao_acordo
        +timedelta(days=2 * 365)

        if self.cleaned_data['data_final_instituicao_fundo_cultura'] > limite:
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        str(limite))

        return self.cleaned_data['data_final_instituicao_fundo_cultura']

    class Meta:
        model = FundoCultura
        exclude = ['situacao_lei_plano']


class PlanoCulturaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('user')
        super(PlanoCulturaForm, self).__init__(*args, **kwargs)

    def clean_data_final_estabelecimento_instancias(self):
        limite = self.usuario.data_publicacao_acordo
        +timedelta(days=2 * 365)

        if self.cleaned_data['data_final_estabelecimento_instancias'] > limite:
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        str(limite))

        return self.cleaned_data['data_final_estabelecimento_instancias']

    def clean_data_final_elaboracao_plano_cultura(self):
        limite = self.usuario.data_publicacao_acordo
        +timedelta(days=2 * 365)

        if self.cleaned_data['data_final_elaboracao_plano_cultura'] > limite:
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        str(limite))

        return self.cleaned_data['data_final_elaboracao_plano_cultura']

    def clean_data_final_aprovacao_plano_cultura(self):
        limite = self.usuario.data_publicacao_acordo
        +timedelta(days=2 * 365)

        if self.cleaned_data['data_final_aprovacao_plano_cultura'] > limite:
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        str(limite))

        return self.cleaned_data['data_final_aprovacao_plano_cultura']

    def clean_data_final_tramitacao_projeto_lei(self):
        limite = self.usuario.data_publicacao_acordo
        +timedelta(days=2 * 365)

        if self.cleaned_data['data_final_tramitacao_projeto_lei'] > limite:
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        str(limite))

        return self.cleaned_data['data_final_tramitacao_projeto_lei']

    def clean_data_final_sancao_lei_plano_cultura(self):
        limite = self.usuario.data_publicacao_acordo
        +timedelta(days=2 * 365)

        if self.cleaned_data['data_final_sancao_lei_plano_cultura'] > limite:
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        str(limite))

        return self.cleaned_data['data_final_sancao_lei_plano_cultura']

    class Meta:
        model = PlanoCultura
        exclude = [
            'situacao_relatorio_diretrizes',
            'situacao_minuta',
            'situacao_ata',
            'situacao_ata_votacao',
            'situacao_lei_plano']
