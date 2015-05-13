from django.db import models
from django.contrib.auth.models import User


TIPO_USUARIO = (
    ('prefeitura', 'Prefeitura'),
    ('responsavel', 'Responsável'),
    ('secretario', 'Secretário'),
)

LISTA_ESTADOS_PROCESSO = (
    ('0', 'Solicitação Expirada'),
    ('1', 'Aguardando envio da documentação'),
    ('2', ''),
    ('3', ''),
    ('4', ''),
    ('5', ''),
    ('6', ''),
    ('7', ''),
)


# Create your models here.
class Uf(models.Model):
    sigla = models.CharField(max_length=2)
    nome = models.CharField(max_length=100)
    regiao = models.CharField(max_length=60)

    def __str__(self):
        return self.nome


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
    cep = models.CharField(max_length=9)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50, blank=True)
    estado = models.ForeignKey('Uf')
    telefone_um = models.CharField(max_length=15)
    telefone_dois = models.CharField(max_length=15, blank=True)
    telefone_tres = models.CharField(max_length=15, blank=True)
    email_institucional_prefeito = models.EmailField()

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
    cpf_usuario = models.CharField(max_length=14, unique=True)
    nome_usuario = models.CharField(max_length=100)
    email_usuario = models.EmailField(unique=True)
    municipio = models.OneToOneField('Municipio', blank=True, null=True)
    responsavel = models.OneToOneField('Responsavel', blank=True, null=True)
    secretario = models.OneToOneField('Secretario', blank=True, null=True)
    estado_processo = models.CharField(
        max_length=1,
        choices=LISTA_ESTADOS_PROCESSO,
        default='1')


class Historico(models.Model):
    usuario = models.OneToOneField(User)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO)
    data_alteracao = models.DateTimeField(auto_now_add=True)
