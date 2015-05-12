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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo_usuario', models.CharField(max_length=20, choices=[('prefeitura', 'Prefeitura'), ('responsavel', 'Responsável'), ('secretario', 'Secretário')])),
                ('data_alteracao', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Prefeitura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cpf_prefeito', models.CharField(max_length=14, unique=True)),
                ('nome_prefeito', models.CharField(max_length=100)),
                ('cnpj_prefeitura', models.CharField(max_length=18, unique=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cpf_responsavel', models.CharField(max_length=14, unique=True)),
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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cpf_secretario', models.CharField(max_length=14, unique=True)),
                ('nome_secretario', models.CharField(max_length=100)),
                ('cargo_secretario', models.CharField(max_length=100)),
                ('instituicao_responsavel', models.CharField(max_length=100)),
                ('telefone_um', models.CharField(max_length=15)),
                ('telefone_dois', models.CharField(blank=True, max_length=15)),
                ('telefone_tres', models.CharField(blank=True, max_length=15)),
                ('email_institucional_secretario', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Uf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sigla', models.CharField(max_length=2)),
                ('nome', models.CharField(max_length=100)),
                ('regiao', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cpf_usuario', models.CharField(max_length=14, unique=True)),
                ('nome_usuario', models.CharField(max_length=100)),
                ('email_usuario', models.EmailField(max_length=254)),
                ('prefeitura', models.OneToOneField(blank=True, null=True, to='adesao.Prefeitura')),
                ('responsavel', models.OneToOneField(blank=True, null=True, to='adesao.Responsavel')),
                ('secretario', models.OneToOneField(blank=True, null=True, to='adesao.Secretario')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='prefeitura',
            name='estado',
            field=models.ForeignKey(to='adesao.Uf'),
        ),
        migrations.AlterUniqueTogether(
            name='prefeitura',
            unique_together=set([('cidade', 'estado')]),
        ),
    ]
