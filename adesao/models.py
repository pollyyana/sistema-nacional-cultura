from django.db import models
from django.contrib.auth.models import User


TIPO_USUARIO = (
    ('prefeitura', 'Prefeitura'),
    ('responsavel', 'Responsável'),
    ('secretario', 'Secretário'),
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
    endereco = models.CharField(max_length=100)
    complemento = models.CharField(max_length=100)
    cep = models.CharField(max_length=9)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.ForeignKey('Uf')
    telefone_um = models.CharField(max_length=15)
    telefone_dois = models.CharField(max_length=15, blank=True)
    telefone_tres = models.CharField(max_length=15, blank=True)
    email_institucional_prefeito = models.EmailField()

    def __str__(self):
        return self.cnpj_prefeito

    class Meta:
        unique_together = ('cidade', 'estado')


class Responsavel(models.Model):
    cpf_responsavel = models.CharField(
        max_length=14,
        unique=True,
        verbose_name='CPF')
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
    prefeitura = models.OneToOneField('Municipio', blank=True, null=True)
    responsavel = models.OneToOneField('Responsavel', blank=True, null=True)
    secretario = models.OneToOneField('Secretario', blank=True, null=True)


class Historico(models.Model):
    usuario = models.OneToOneField(User)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO)
    data_alteracao = models.DateTimeField(auto_now_add=True)
