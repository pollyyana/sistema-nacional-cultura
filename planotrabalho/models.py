from django.db import models

# Create your models here.
SITUACAO_ENVIO = (
    (0, 'Em preenchimento'),
    (1, 'Avaliando anexo'),
    (2, 'Concluída')
    )
SITUACAO_CONSELHEIRO = (
    ('1', 'Habilitado'),
    ('0', 'Desabilitado')
    )


class PlanoTrabalho(models.Model):
    criacao_sistema = models.OneToOneField(
        'CriacaoSistema',
        blank=True,
        null=True)
    orgao_gestor = models.OneToOneField(
        'OrgaoGestor',
        blank=True,
        null=True)
    conselho_cultural = models.OneToOneField(
        'ConselhoCultural',
        blank=True,
        null=True)
    fundo_cultura = models.OneToOneField(
        'FundoCultura',
        blank=True,
        null=True)
    plano_cultura = models.OneToOneField(
        'PlanoCultura',
        blank=True,
        null=True)

    def __str__(self):
        return str(self.id)


class CriacaoSistema(models.Model):
    data_final_elaboracao_projeto_lei = models.DateField()
    minuta_projeto_lei = models.FileField(
        upload_to='minuta_lei',
        max_length=255,
        blank=True,
        null=True)
    situacao_minuta = models.CharField(
        max_length=1,
        choices=SITUACAO_ENVIO,
        default=0)
    data_final_sancao_lei = models.DateField()
    lei_sistema_cultura = models.FileField(
        upload_to='leis_sistema_cultura',
        max_length=255,
        blank=True,
        null=True)
    situacao_lei_sistema = models.CharField(
        max_length=1,
        choices=SITUACAO_ENVIO,
        default=0)


class OrgaoGestor(models.Model):
    data_final_estruturacao_secretaria = models.DateField()
    relatorio_atividade_secretaria = models.FileField(
        upload_to='relatorio_atividades',
        max_length=255,
        blank=True,
        null=True)
    situacao_relatorio_secretaria = models.CharField(
        max_length=1,
        choices=SITUACAO_ENVIO,
        default=0)


class ConselhoCultural(models.Model):
    data_final_instalacao_conselho = models.DateField()
    ata_regimento_aprovado = models.FileField(
        upload_to='regimentos',
        max_length=255,
        blank=True,
        null=True)
    situacao_ata = models.CharField(
        max_length=1,
        choices=SITUACAO_ENVIO,
        default=0)


class FundoCultura(models.Model):
    data_final_instituicao_fundo_cultura = models.DateField()
    cnpj_fundo_cultura = models.CharField(
        max_length=18,
        verbose_name='CNPJ',
        blank=True,
        null=True,
        default=None)
    lei_fundo_cultura = models.FileField(
        upload_to='lei_fundo_cultura',
        max_length=255,
        blank=True,
        null=True)
    situacao_lei_plano = models.CharField(
        max_length=1,
        choices=SITUACAO_ENVIO,
        default=0)


class PlanoCultura(models.Model):
    data_final_estabelecimento_instancias = models.DateField()
    relatorio_diretrizes_aprovadas = models.FileField(
        upload_to='relatorio_diretrizes',
        max_length=255,
        blank=True,
        null=True)
    situacao_relatorio_diretrizes = models.CharField(
        max_length=1,
        choices=SITUACAO_ENVIO,
        default=0)
    data_final_elaboracao_plano_cultura = models.DateField()
    minuta_preparada = models.FileField(
        upload_to='minuta_preparada',
        max_length=255,
        blank=True,
        null=True)
    situacao_minuta = models.CharField(
        max_length=1,
        choices=SITUACAO_ENVIO,
        default=0)
    data_final_aprovacao_plano_cultura = models.DateField()
    ata_reuniao_aprovacao_plano = models.FileField(
        upload_to='ata_aprovacao_plano',
        max_length=255,
        blank=True,
        null=True)
    situacao_ata = models.CharField(
        max_length=1,
        choices=SITUACAO_ENVIO,
        default=0)
    data_final_tramitacao_projeto_lei = models.DateField(blank=True, null=True)
    ata_votacao_projeto_lei = models.FileField(
        upload_to='ata_votacao_lei',
        max_length=255,
        blank=True,
        null=True)
    situacao_ata_votacao = models.CharField(
        max_length=1,
        choices=SITUACAO_ENVIO,
        default=0)
    data_final_sancao_lei_plano_cultura = models.DateField()
    lei_plano_cultura = models.FileField(
        upload_to='lei_plano_cultura',
        max_length=255,
        blank=True,
        null=True)
    situacao_lei_plano = models.CharField(
        max_length=1,
        choices=SITUACAO_ENVIO,
        default=0)


class Conselheiro(models.Model):
    nome = models.CharField(max_length=100)
    segmento = models.CharField(max_length=255)
    email = models.EmailField(unique=False)
    situacao = models.CharField(
        blank=True,
        null=True,
        max_length=1,
        choices=SITUACAO_CONSELHEIRO,
        default=1)
    data_cadastro = models.DateField(blank=True, null=True)
    data_situacao = models.DateField(blank=True, null=True)
    conselho = models.ForeignKey('ConselhoCultural')
