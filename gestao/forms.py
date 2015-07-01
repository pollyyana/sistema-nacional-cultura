from django import forms
from django.forms import ModelForm

from adesao.models import Usuario, Historico
from planotrabalho.models import PlanoTrabalho

from .utils import enviar_email_alteracao_situacao


class AlterarSituacao(ModelForm):
    justificativa = forms.CharField(max_length="255", required=False)

    def save(self, commit=True):
        usuario = super(AlterarSituacao, self).save(commit=False)
        dir(usuario)
        enviar_email_alteracao_situacao(usuario)
        historico = Historico()
        historico.usuario = usuario

        if usuario.estado_processo == '3':
            historico.descricao = self.cleaned_data['justificativa']

        if usuario.estado_processo == '6':
            if usuario.plano_trabalho is None:
                plano_trabalho = PlanoTrabalho()

                if commit:
                    plano_trabalho.save()

                usuario.plano_trabalho = plano_trabalho
                print(usuario.plano_trabalho)

        if commit:
            usuario.save()
            historico.save()

    class Meta:
        model = Usuario
        fields = ('estado_processo', 'data_publicacao_acordo')
