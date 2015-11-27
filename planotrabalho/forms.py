from django import forms
from django.forms import ModelForm
from django.forms.widgets import FileInput

from .models import CriacaoSistema, OrgaoGestor, ConselhoCultural
from .models import FundoCultura, PlanoCultura, Conselheiro
from .utils import validar_cnpj, add_anos

SETORIAIS = (
    (1, 'Arquitetura e Urbanismo'),
    (2, 'Arquivos'),
    (3, 'Arte Digital'),
    (4, 'Artes Visuais'),
    (5, 'Artesanato'),
    (6, 'Audiovisual'),
    (7, 'Circo'),
    (8, 'Culturas Afro-brasileiras'),
    (9, 'Culturas dos Povos Indígenas'),
    (10, 'Culturas Populares'),
    (11, 'Dança'),
    (12, 'Design'),
    (13, 'Literatura, Livro e Leitura'),
    (14, 'Moda'),
    (15, 'Museus'),
    (16, 'Música Erudita'),
    (17, 'Música Popular'),
    (18, 'Patrimônio Imaterial'),
    (19, 'Patrimônio Material'),
    (20, 'Teatro')
    )


class CriarSistemaForm(ModelForm):
    minuta_projeto_lei = forms.FileField(required=False, widget=FileInput)
    lei_sistema_cultura = forms.FileField(required=False, widget=FileInput)

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('user')
        super(CriarSistemaForm, self).__init__(*args, **kwargs)

    def clean_data_final_elaboracao_projeto_lei(self):
        if not self.usuario.data_publicacao_acordo:
            return self.cleaned_data['data_final_elaboracao_projeto_lei']
        if not self.cleaned_data['data_final_elaboracao_projeto_lei']:
            return self.cleaned_data['data_final_elaboracao_projeto_lei']

        limite = add_anos(self.usuario.data_publicacao_acordo, self.usuario.prazo)

        if self.cleaned_data['data_final_elaboracao_projeto_lei'] > limite:
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        limite.strftime("%d/%m/%Y"))

        return self.cleaned_data['data_final_elaboracao_projeto_lei']

    def clean_data_final_sancao_lei(self):
        if not self.usuario.data_publicacao_acordo:
            return self.cleaned_data['data_final_sancao_lei']
        if not self.cleaned_data['data_final_sancao_lei']:
            return self.cleaned_data['data_final_sancao_lei']

        limite = add_anos(self.usuario.data_publicacao_acordo, self.usuario.prazo)

        if self.cleaned_data['data_final_sancao_lei'] > (limite):
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        limite.strftime("%d/%m/%Y"))

        return self.cleaned_data['data_final_sancao_lei']

    def save(self, commit=True, *args, **kwargs):
        sistema = super(CriarSistemaForm, self).save(commit=False)
        if 'minuta_projeto_lei' in self.changed_data:
            sistema.situacao_minuta = 1

        if 'lei_sistema_cultura' in self.changed_data:
            sistema.situacao_lei_sistema = 1

        if commit:
            sistema.save()
        return sistema

    class Meta:
        model = CriacaoSistema
        exclude = ['situacao_minuta', 'situacao_lei_sistema']


class OrgaoGestorForm(ModelForm):
    relatorio_atividade_secretaria = forms.FileField(
        required=False, widget=FileInput)

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('user')
        super(OrgaoGestorForm, self).__init__(*args, **kwargs)

    def clean_data_final_estruturacao_secretaria(self):
        if not self.usuario.data_publicacao_acordo:
            return self.cleaned_data['data_final_estruturacao_secretaria']
        if not self.cleaned_data['data_final_estruturacao_secretaria']:
            return self.cleaned_data['data_final_estruturacao_secretaria']

        limite = add_anos(self.usuario.data_publicacao_acordo, self.usuario.prazo)

        if self.cleaned_data['data_final_estruturacao_secretaria'] > limite:
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        limite.strftime("%d/%m/%Y"))

        return self.cleaned_data['data_final_estruturacao_secretaria']

    def save(self, commit=True, *args, **kwargs):
        orgao = super(OrgaoGestorForm, self).save(commit=False)
        if 'relatorio_atividade_secretaria' in self.changed_data:
            orgao.situacao_relatorio_secretaria = 1

        if commit:
            orgao.save()
        return orgao

    class Meta:
        model = OrgaoGestor
        exclude = ['situacao_relatorio_secretaria']


class ConselhoCulturalForm(ModelForm):
    ata_regimento_aprovado = forms.FileField(required=False, widget=FileInput)

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('user')
        super(ConselhoCulturalForm, self).__init__(*args, **kwargs)

    def clean_data_final_instalacao_conselho(self):
        if not self.usuario.data_publicacao_acordo:
            return self.cleaned_data['data_final_instalacao_conselho']
        if not self.cleaned_data['data_final_instalacao_conselho']:
            return self.cleaned_data['data_final_instalacao_conselho']

        limite = add_anos(self.usuario.data_publicacao_acordo, self.usuario.prazo)

        if self.cleaned_data['data_final_instalacao_conselho'] > limite:
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        limite.strftime("%d/%m/%Y"))

        return self.cleaned_data['data_final_instalacao_conselho']

    def save(self, commit=True, *args, **kwargs):
        conselho = super(ConselhoCulturalForm, self).save(commit=False)
        if 'ata_regimento_aprovado' in self.changed_data:
            conselho.situacao_ata = 1

        if commit:
            conselho.save()
            nomes = self.data.getlist('conselheiro')
            emails = self.data.getlist('email')
            segmentos = self.data.getlist('segmento')
            outros_segmentos = self.data.getlist('outros_segmento')
            for nome, email, segmento, outros_segmento in zip(nomes, emails, segmentos, outros_segmentos):
                if nome and email and segmento:
                    segmento = dict(SETORIAIS)[int(segmento)] if segmento != '21' else outros_segmento
                    Conselheiro.objects.get_or_create(nome=nome, email=email, segmento=segmento, conselho=conselho)
                else:
                    Conselheiro.objects.filter(nome=nome, email=email, conselho=conselho).delete()
            Conselheiro.objects.filter(conselho=conselho).exclude(email__in=emails).delete()
        return conselho

    class Meta:
        model = ConselhoCultural
        exclude = ['situacao_ata']


class FundoCulturaForm(ModelForm):
    lei_fundo_cultura = forms.FileField(required=False, widget=FileInput)

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('user')
        super(FundoCulturaForm, self).__init__(*args, **kwargs)

    def clean_data_final_instituicao_fundo_cultura(self):
        if not self.usuario.data_publicacao_acordo:
            return self.cleaned_data['data_final_instituicao_fundo_cultura']
        if not self.cleaned_data['data_final_instituicao_fundo_cultura']:
            return self.cleaned_data['data_final_instituicao_fundo_cultura']

        limite = add_anos(self.usuario.data_publicacao_acordo, self.usuario.prazo)

        if self.cleaned_data['data_final_instituicao_fundo_cultura'] > limite:
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        limite.strftime("%d/%m/%Y"))

        return self.cleaned_data['data_final_instituicao_fundo_cultura']

    def clean_cnpj_fundo_cultura(self):
        cnpj = self.cleaned_data['cnpj_fundo_cultura']
        if 'lei_fundo_cultura' in self.changed_data and not cnpj:
            raise forms.ValidationError('CNPJ é obrigatório')
        if cnpj:
            if FundoCultura.objects.filter(cnpj_fundo_cultura=cnpj) and 'cnpj_fundo_cultura' in self.changed_data:
                raise forms.ValidationError(
                    'Já existe um Fundo de Cultura com este CNPJ cadastrado')
            elif not validar_cnpj(cnpj):
                raise forms.ValidationError('CNPJ inválido')

        return self.cleaned_data['cnpj_fundo_cultura']

    def save(self, commit=True, *args, **kwargs):
        fundo = super(FundoCulturaForm, self).save(commit=False)
        if 'lei_fundo_cultura' in self.changed_data and self.is_valid:
            fundo.situacao_lei_plano = 1

        if commit:
            fundo.save()
        return fundo

    class Meta:
        model = FundoCultura
        exclude = ['situacao_lei_plano']


class PlanoCulturaForm(ModelForm):
    relatorio_diretrizes_aprovadas = forms.FileField(
        required=False, widget=FileInput)
    minuta_preparada = forms.FileField(required=False, widget=FileInput)
    ata_reuniao_aprovacao_plano = forms.FileField(
        required=False, widget=FileInput)
    lei_plano_cultura = forms.FileField(required=False, widget=FileInput)

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('user')
        super(PlanoCulturaForm, self).__init__(*args, **kwargs)

    def clean_data_final_estabelecimento_instancias(self):
        if not self.usuario.data_publicacao_acordo:
            return self.cleaned_data['data_final_estabelecimento_instancias']
        if not self.cleaned_data['data_final_estabelecimento_instancias']:
            return self.cleaned_data['data_final_estabelecimento_instancias']

        limite = add_anos(self.usuario.data_publicacao_acordo, self.usuario.prazo)

        if self.cleaned_data['data_final_estabelecimento_instancias'] > limite:
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        limite.strftime("%d/%m/%Y"))

        return self.cleaned_data['data_final_estabelecimento_instancias']

    def clean_data_final_elaboracao_plano_cultura(self):
        if not self.usuario.data_publicacao_acordo:
            return self.cleaned_data['data_final_elaboracao_plano_cultura']
        if not self.cleaned_data['data_final_elaboracao_plano_cultura']:
            return self.cleaned_data['data_final_elaboracao_plano_cultura']

        limite = add_anos(self.usuario.data_publicacao_acordo, self.usuario.prazo)

        if self.cleaned_data['data_final_elaboracao_plano_cultura'] > limite:
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        limite.strftime("%d/%m/%Y"))

        return self.cleaned_data['data_final_elaboracao_plano_cultura']

    def clean_data_final_aprovacao_plano_cultura(self):
        if not self.usuario.data_publicacao_acordo:
            return self.cleaned_data['data_final_aprovacao_plano_cultura']
        if not self.cleaned_data['data_final_aprovacao_plano_cultura']:
            return self.cleaned_data['data_final_aprovacao_plano_cultura']

        limite = add_anos(self.usuario.data_publicacao_acordo, self.usuario.prazo)

        if self.cleaned_data['data_final_aprovacao_plano_cultura'] > limite:
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        limite.strftime("%d/%m/%Y"))

        return self.cleaned_data['data_final_aprovacao_plano_cultura']

    def clean_data_final_sancao_lei_plano_cultura(self):
        if not self.usuario.data_publicacao_acordo:
            return self.cleaned_data['data_final_sancao_lei_plano_cultura']
        if not self.cleaned_data['data_final_sancao_lei_plano_cultura']:
            return self.cleaned_data['data_final_sancao_lei_plano_cultura']

        limite = add_anos(self.usuario.data_publicacao_acordo, self.usuario.prazo)

        if self.cleaned_data['data_final_sancao_lei_plano_cultura'] > limite:
            raise forms.ValidationError('A data deve ser anterior a ' +
                                        limite.strftime("%d/%m/%Y"))

        return self.cleaned_data['data_final_sancao_lei_plano_cultura']

    def save(self, commit=True, *args, **kwargs):
        plano = super(PlanoCulturaForm, self).save(commit=False)
        if 'relatorio_diretrizes_aprovadas' in self.changed_data:
            plano.situacao_relatorio_diretrizes = 1

        if 'minuta_preparada' in self.changed_data:
            plano.situacao_minuta = 1

        if 'ata_reuniao_aprovacao_plano' in self.changed_data:
            plano.situacao_ata = 1

        if 'ata_votacao_projeto_lei' in self.changed_data:
            plano.situacao_ata_votacao = 1

        if 'lei_plano_cultura' in self.changed_data:
            plano.situacao_lei_plano = 1

        if commit:
            plano.save()
        return plano

    class Meta:
        model = PlanoCultura
        exclude = [
            'situacao_relatorio_diretrizes',
            'situacao_minuta',
            'situacao_ata',
            'situacao_ata_votacao',
            'situacao_lei_plano']
