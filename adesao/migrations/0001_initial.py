# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Historico',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('tipo_usuario', models.CharField(choices=[('prefeitura', 'Prefeitura'), ('responsavel', 'Responsável'), ('secretario', 'Secretário')], max_length=20)),
                ('data_alteracao', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('cpf_prefeito', models.CharField(unique=True, verbose_name='CPF', max_length=14)),
                ('nome_prefeito', models.CharField(max_length=100)),
                ('cnpj_prefeitura', models.CharField(unique=True, verbose_name='CNPJ', max_length=18)),
                ('rg_prefeito', models.CharField(verbose_name='RG', max_length=15)),
                ('orgao_expeditor_rg', models.CharField(max_length=50)),
                ('endereco', models.CharField(max_length=100)),
                ('complemento', models.CharField(max_length=100)),
                ('cep', models.CharField(max_length=9)),
                ('bairro', models.CharField(max_length=50)),
                ('cidade', models.CharField(max_length=50)),
                ('telefone_um', models.CharField(max_length=15)),
                ('telefone_dois', models.CharField(blank=True, max_length=15)),
                ('telefone_tres', models.CharField(blank=True, max_length=15)),
                ('email_institucional_prefeito', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Responsavel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('cpf_responsavel', models.CharField(unique=True, verbose_name='CPF', max_length=14)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('cpf_secretario', models.CharField(unique=True, verbose_name='CPF', max_length=14)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('sigla', models.CharField(max_length=2)),
                ('nome', models.CharField(max_length=100)),
                ('regiao', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('cpf_usuario', models.CharField(unique=True, max_length=14)),
                ('nome_usuario', models.CharField(max_length=100)),
                ('email_usuario', models.EmailField(unique=True, max_length=254)),
                ('estado_processo', models.CharField(default='1', choices=[('0', 'Solicitação Expirada'), ('1', 'Aguardando envio da documentação'), ('2', ''), ('3', ''), ('4', ''), ('5', ''), ('6', ''), ('7', '')], max_length=1)),
                ('municipio', models.OneToOneField(blank=True, null=True, to='adesao.Municipio')),
                ('responsavel', models.OneToOneField(blank=True, null=True, to='adesao.Responsavel')),
                ('secretario', models.OneToOneField(blank=True, null=True, to='adesao.Secretario')),
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
