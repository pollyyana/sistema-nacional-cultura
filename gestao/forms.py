from threading import Thread
from django import forms
from django.core.mail import send_mail
from django.forms import ModelForm

from adesao.models import Usuario, Historico
from planotrabalho.models import PlanoTrabalho

from .utils import enviar_email_alteracao_situacao

from ckeditor.widgets import CKEditorWidget


class AlterarSituacao(ModelForm):
    justificativa = forms.CharField(max_length="255", required=False)

    def save(self, commit=True):
        usuario = super(AlterarSituacao, self).save(commit=False)
        historico = Historico()
        historico.usuario = usuario
        historico.situacao = self.cleaned_data['estado_processo']

        if self.cleaned_data['estado_processo'] == '3':
            historico.descricao = self.cleaned_data['justificativa']

        if self.cleaned_data['estado_processo'] == '6':
            if usuario.plano_trabalho is None:
                plano_trabalho = PlanoTrabalho()

                if commit:
                    plano_trabalho.save()

                usuario.plano_trabalho = plano_trabalho
                print(usuario.plano_trabalho)

        if commit:
            usuario.save()
            historico.save()
            enviar_email_alteracao_situacao(usuario, historico)

    class Meta:
        model = Usuario
        fields = ('estado_processo', 'data_publicacao_acordo')


class DiligenciaForm(forms.Form):
    diligencia = forms.CharField(required=False, widget=CKEditorWidget())

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super(DiligenciaForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        subject = '[Sistema Nacional de Cultura] Diligência em anexo'
        Thread(target=send_mail, args=(
            subject,
            self.cleaned_data['diligencia'],
            'naoresponda@cultura.gov.br',
            [self.usuario.user.email],),
            kwargs = {
                'fail_silently': 'False',
                'html_message': self.cleaned_data['diligencia']}
        ).start()
