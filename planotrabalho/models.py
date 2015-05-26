from django.db import models

# Create your models here.


class PlanoTrabalho(models.Model):
    criacao_sistema = models.OneToOneField('CriacaoSistema')
    orgao_gestor = models.OneToOneField('OrgaoGestor')
    conselho_cultural = models.OneToOneField('ConselhoCultural')
    fundo_cultura = models.OneToOneField('FundoCultura')
    plano_cultura = models.OneToOneField('PlanoCultura')


class CriacaoSistema(models.Model):
    data_final_elaboracao_projeto_lei = models.DateField()
    minuta_projeto_lei = models.FileField(
        upload_to='minuta_lei',
        blank=True,
        null=True)
    data_final_sancao_lei = models.DateField()
    lei_sistema_cultura = models.FileField(
        upload_to='leis_sistema_cultura',
        blank=True,
        null=True)


class OrgaoGestor(models.Model):
    data_final_estruturacao_secretaria = models.DateField()
    relatorio_atividade_secretaria = models.FileField(
        upload_to='relatorio_atividades',
        blank=True,
        null=True)


class ConselhoCultural(models.Model):
    data_final_instalacao_conselho = models.DateField()
    ata_regimento_aprovado = models.FileField(
        upload_to='regimentos',
        blank=True,
        null=True)


class FundoCultura(models.Model):
    data_final_instituicao_fundo_cultura = models.DateField()
    cnpj_fundo_cultura = models.CharField(
        max_length=18,
        unique=True,
        verbose_name='CNPJ',
        blank=True,
        null=True)
    lei_fundo_cultura = models.FileField(
        upload_to='lei_fundo_cultura',
        blank=True,
        null=True)


class PlanoCultura(models.Model):
    data_final_estabelecimento_instancias = models.DateField()
    relatorio_diretrizes_aprovadas = models.FileField(
        upload_to='relatorio_diretrizes',
        blank=True,
        null=True)
    data_final_elaboracao_plano_cultura = models.DateField()
    minuta_preparada = models.FileField(
        upload_to='minuta_preparada',
        blank=True,
        null=True)
    data_final_aprovacao_plano_cultura = models.DateField()
    ata_reuniao_aprovacao_plano = models.FileField(
        upload_to='ata_aprovacao_plano',
        blank=True,
        null=True)
    data_final_tramitacao_projeto_lei = models.DateField()
    ata_votacao_projeto_lei = models.FileField(
        upload_to='ata_votacao_lei',
        blank=True,
        null=True)
    data_final_sancao_lei_plano_cultura = models.DateField()
    lei_plano_cultura = models.FileField(
        upload_to='lei_plano_cultura',
        blank=True,
        null=True)
