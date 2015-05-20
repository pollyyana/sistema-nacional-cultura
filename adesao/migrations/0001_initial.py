# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import validatedfile.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cidade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('codigo_ibge', models.IntegerField(unique=True)),
                ('nome_municipio', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Historico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('data_alteracao', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('cpf_prefeito', models.CharField(verbose_name='CPF', unique=True, max_length=14)),
                ('nome_prefeito', models.CharField(max_length=100)),
                ('cnpj_prefeitura', models.CharField(verbose_name='CNPJ', unique=True, max_length=18)),
                ('rg_prefeito', models.CharField(verbose_name='RG', max_length=15)),
                ('orgao_expeditor_rg', models.CharField(max_length=50)),
                ('endereco', models.CharField(max_length=100)),
                ('complemento', models.CharField(max_length=100)),
                ('cep', models.CharField(max_length=9)),
                ('bairro', models.CharField(max_length=50)),
                ('telefone_um', models.CharField(max_length=15)),
                ('telefone_dois', models.CharField(blank=True, max_length=15)),
                ('telefone_tres', models.CharField(blank=True, max_length=15)),
                ('email_institucional_prefeito', models.EmailField(max_length=254)),
                ('termo_posse_prefeito', validatedfile.fields.ValidatedFileField(upload_to='termo_posse')),
                ('rg_copia_prefeito', validatedfile.fields.ValidatedFileField(upload_to='rg_copia')),
                ('cpf_copia_prefeito', validatedfile.fields.ValidatedFileField(upload_to='cpf_copia')),
                ('cidade', models.ForeignKey(to='adesao.Cidade', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Responsavel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('cpf_responsavel', models.CharField(verbose_name='CPF', unique=True, max_length=14)),
                ('rg_responsavel', models.CharField(verbose_name='RG', max_length=15)),
                ('orgao_expeditor_rg', models.CharField(max_length=50)),
                ('nome_responsavel', models.CharField(max_length=100)),
                ('cargo_responsavel', models.CharField(max_length=100)),
                ('instituicao_responsavel', models.CharField(max_length=100)),
                ('telefone_um', models.CharField(max_length=15)),
                ('telefone_dois', models.CharField(blank=True, max_length=15)),
                ('telefone_tres', models.CharField(blank=True, max_length=15)),
                ('email_institucional_responsavel', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Secretario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('cpf_secretario', models.CharField(verbose_name='CPF', unique=True, max_length=14)),
                ('rg_secretario', models.CharField(verbose_name='RG', max_length=15)),
                ('orgao_expeditor_rg', models.CharField(max_length=50)),
                ('nome_secretario', models.CharField(max_length=100)),
                ('cargo_secretario', models.CharField(max_length=100)),
                ('instituicao_secretario', models.CharField(max_length=100)),
                ('telefone_um', models.CharField(max_length=15)),
                ('telefone_dois', models.CharField(blank=True, max_length=15)),
                ('telefone_tres', models.CharField(blank=True, max_length=15)),
                ('email_institucional_secretario', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Uf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('codigo_ibge', models.IntegerField()),
                ('sigla', models.CharField(max_length=2)),
                ('nome_uf', models.CharField(max_length=100)),
                ('regiao', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nome_usuario', models.CharField(max_length=100)),
                ('estado_processo', models.CharField(max_length=1, default='1', choices=[('0', 'Solicitação Expirada'), ('1', 'Aguardando envio da documentação'), ('2', ''), ('3', ''), ('4', ''), ('5', ''), ('6', 'Acordo publicado'), ('7', 'Responsável confirmado')])),
                ('data_publicacao_acordo', models.DateField(null=True, blank=True)),
                ('municipio', models.OneToOneField(null=True, blank=True, to='adesao.Municipio')),
                ('responsavel', models.OneToOneField(null=True, blank=True, to='adesao.Responsavel')),
                ('secretario', models.OneToOneField(null=True, blank=True, to='adesao.Secretario')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='secretario',
            name='estado_expeditor',
            field=models.ForeignKey(to='adesao.Uf'),
        ),
        migrations.AddField(
            model_name='responsavel',
            name='estado_expeditor',
            field=models.ForeignKey(to='adesao.Uf'),
        ),
        migrations.AddField(
            model_name='municipio',
            name='estado',
            field=models.ForeignKey(to='adesao.Uf'),
        ),
        migrations.AddField(
            model_name='municipio',
            name='estado_expeditor',
            field=models.ForeignKey(to='adesao.Uf', related_name='estado_expeditor'),
        ),
        migrations.AlterUniqueTogether(
            name='municipio',
            unique_together=set([('cidade', 'estado')]),
        ),
    ]
