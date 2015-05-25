from django.db import models
from django.contrib.auth.models import User

from smart_selects.db_fields import ChainedForeignKey


LISTA_ESTADOS_PROCESSO = (
    ('0', 'Solicitação Expirada'),
    ('1', 'Aguardando envio da documentação'),
    ('2', ''),
    ('3', ''),
    ('4', ''),
    ('5', ''),
    ('6', 'Acordo publicado'),
    ('7', 'Responsável confirmado'),
)


# Create your models here.
class Uf(models.Model):
    codigo_ibge = models.IntegerField(primary_key=True)
    sigla = models.CharField(max_length=2)
    nome_uf = models.CharField(max_length=100)

    def __str__(self):
        return self.sigla

    class Meta:
        ordering = ['sigla']


class Cidade(models.Model):
    codigo_ibge = models.IntegerField(unique=True)
    uf = models.ForeignKey('Uf', to_field='codigo_ibge')
    nome_municipio = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_municipio

    class Meta:
        ordering = ['nome_municipio']


class Municipio(models.Model):
    cpf_prefeito = models.CharField(
        max_length=14,
        unique=True,
        verbose_name='CPF')
    nome_prefeito = models.CharField(max_length=100)
    cnpj_prefeitura = models.CharField(
        max_length=18,
        unique=True,
        verbose_name='CNPJ')
    rg_prefeito = models.CharField(max_length=15, verbose_name='RG')
    orgao_expeditor_rg = models.CharField(max_length=50)
    estado_expeditor = models.ForeignKey('Uf', related_name='estado_expeditor')
    endereco = models.CharField(max_length=100)
    complemento = models.CharField(max_length=100)
    cep = models.CharField(max_length=10)
    bairro = models.CharField(max_length=50)
    estado = models.ForeignKey('Uf')
    cidade = ChainedForeignKey(
        Cidade,
        chained_field='estado',
        chained_model_field='uf',
        show_all=False,
        auto_choose=True,
        blank=True,
        null=True
    )
    telefone_um = models.CharField(max_length=15)
    telefone_dois = models.CharField(max_length=15, blank=True)
    telefone_tres = models.CharField(max_length=15, blank=True)
    email_institucional_prefeito = models.EmailField()
    termo_posse_prefeito = models.FileField(upload_to='termo_posse')
    rg_copia_prefeito = models.FileField(upload_to='rg_copia')
    cpf_copia_prefeito = models.FileField(upload_to='cpf_copia')

    def __str__(self):
        return self.cnpj_prefeitura

    class Meta:
        unique_together = ('cidade', 'estado')


class Responsavel(models.Model):
    cpf_responsavel = models.CharField(
        max_length=14,
        unique=True,
        verbose_name='CPF')
    rg_responsavel = models.CharField(max_length=15, verbose_name='RG')
    orgao_expeditor_rg = models.CharField(max_length=50)
    estado_expeditor = models.ForeignKey('Uf')
    nome_responsavel = models.CharField(max_length=100)
    cargo_responsavel = models.CharField(max_length=100)
    instituicao_responsavel = models.CharField(max_length=100)
    telefone_um = models.CharField(max_length=15)
    telefone_dois = models.CharField(max_length=15, blank=True)
    telefone_tres = models.CharField(max_length=15, blank=True)
    email_institucional_responsavel = models.EmailField()

    def __str__(self):
        return self.cpf_responsavel


class Secretario(models.Model):
    cpf_secretario = models.CharField(
        max_length=14,
        unique=True,
        verbose_name='CPF')
    rg_secretario = models.CharField(max_length=15, verbose_name='RG')
    orgao_expeditor_rg = models.CharField(max_length=50)
    estado_expeditor = models.ForeignKey('Uf')
    nome_secretario = models.CharField(max_length=100)
    cargo_secretario = models.CharField(max_length=100)
    instituicao_secretario = models.CharField(max_length=100)
    telefone_um = models.CharField(max_length=15)
    telefone_dois = models.CharField(max_length=15, blank=True)
    telefone_tres = models.CharField(max_length=15, blank=True)
    email_institucional_secretario = models.EmailField()

    def __str__(self):
        return self.cpf_secretario


class Usuario(models.Model):
    user = models.OneToOneField(User)
    nome_usuario = models.CharField(max_length=100)
    municipio = models.OneToOneField('Municipio', blank=True, null=True)
    responsavel = models.OneToOneField('Responsavel', blank=True, null=True)
    secretario = models.OneToOneField('Secretario', blank=True, null=True)
    estado_processo = models.CharField(
        max_length=1,
        choices=LISTA_ESTADOS_PROCESSO,
        default='1')
    data_publicacao_acordo = models.DateField(blank=True, null=True)
    codigo_ativacao = models.CharField(max_length=12, unique=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Historico(models.Model):
    usuario = models.OneToOneField(User)
    data_alteracao = models.DateTimeField(auto_now_add=True)
