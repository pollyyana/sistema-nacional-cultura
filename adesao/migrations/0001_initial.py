# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('planotrabalho', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cidade',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('codigo_ibge', models.IntegerField(unique=True)),
                ('nome_municipio', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['nome_municipio'],
            },
        ),
        migrations.CreateModel(
            name='Historico',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('data_alteracao', models.DateTimeField(auto_now_add=True)),
                ('arquivo', models.FileField(null=True, upload_to='historico', blank=True)),
                ('descricao', models.TextField(null=True, blank=True)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('cpf_prefeito', models.CharField(max_length=14, unique=True, verbose_name='CPF')),
                ('nome_prefeito', models.CharField(max_length=100)),
                ('cnpj_prefeitura', models.CharField(max_length=18, unique=True, verbose_name='CNPJ')),
                ('rg_prefeito', models.CharField(max_length=15, verbose_name='RG')),
                ('orgao_expeditor_rg', models.CharField(max_length=50)),
                ('endereco', models.CharField(max_length=100)),
                ('complemento', models.CharField(max_length=100)),
                ('cep', models.CharField(max_length=10)),
                ('bairro', models.CharField(max_length=50)),
                ('telefone_um', models.CharField(max_length=15)),
                ('telefone_dois', models.CharField(max_length=15, blank=True)),
                ('telefone_tres', models.CharField(max_length=15, blank=True)),
                ('email_institucional_prefeito', models.EmailField(max_length=254)),
                ('termo_posse_prefeito', models.FileField(max_length=255, null=True, upload_to='termo_posse', blank=True)),
                ('rg_copia_prefeito', models.FileField(max_length=255, null=True, upload_to='rg_copia', blank=True)),
                ('cpf_copia_prefeito', models.FileField(max_length=255, null=True, upload_to='cpf_copia', blank=True)),
                ('cidade', smart_selects.db_fields.ChainedForeignKey(blank=True, chained_model_field='uf', null=True, chained_field='estado', to='adesao.Cidade')),
            ],
        ),
        migrations.CreateModel(
            name='Responsavel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('cpf_responsavel', models.CharField(max_length=14, unique=True, verbose_name='CPF')),
                ('rg_responsavel', models.CharField(max_length=15, verbose_name='RG')),
                ('orgao_expeditor_rg', models.CharField(max_length=50)),
                ('nome_responsavel', models.CharField(max_length=100)),
                ('cargo_responsavel', models.CharField(max_length=100)),
                ('instituicao_responsavel', models.CharField(max_length=100)),
                ('telefone_um', models.CharField(max_length=15)),
                ('telefone_dois', models.CharField(max_length=15, blank=True)),
                ('telefone_tres', models.CharField(max_length=15, blank=True)),
                ('email_institucional_responsavel', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Secretario',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('cpf_secretario', models.CharField(max_length=14, unique=True, verbose_name='CPF')),
                ('rg_secretario', models.CharField(max_length=15, verbose_name='RG')),
                ('orgao_expeditor_rg', models.CharField(max_length=50)),
                ('nome_secretario', models.CharField(max_length=100)),
                ('cargo_secretario', models.CharField(max_length=100)),
                ('instituicao_secretario', models.CharField(max_length=100)),
                ('telefone_um', models.CharField(max_length=15)),
                ('telefone_dois', models.CharField(max_length=15, blank=True)),
                ('telefone_tres', models.CharField(max_length=15, blank=True)),
                ('email_institucional_secretario', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Uf',
            fields=[
                ('codigo_ibge', models.IntegerField(serialize=False, primary_key=True)),
                ('sigla', models.CharField(max_length=2)),
                ('nome_uf', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['sigla'],
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nome_usuario', models.CharField(max_length=100)),
                ('estado_processo', models.CharField(max_length=1, choices=[('0', 'Solicitação Expirada'), ('1', 'Aguardando envio da documentação'), ('2', 'Documentação Recebida - Aguarda Análise'), ('3', 'Diligência Documental'), ('4', 'Encaminhado para assinatura do Secretário SAI'), ('5', 'Aguarda Publicação no DOU'), ('6', 'Publicado no DOU'), ('7', 'Responsável confirmado')], default='1')),
                ('data_publicacao_acordo', models.DateField(null=True, blank=True)),
                ('codigo_ativacao', models.CharField(max_length=12, unique=True)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('municipio', models.OneToOneField(blank=True, null=True, to='adesao.Municipio')),
                ('plano_trabalho', models.OneToOneField(blank=True, null=True, to='planotrabalho.PlanoTrabalho')),
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
            field=models.ForeignKey(related_name='estado_expeditor', to='adesao.Uf'),
        ),
        migrations.AddField(
            model_name='cidade',
            name='uf',
            field=models.ForeignKey(to='adesao.Uf'),
        ),
        migrations.AlterUniqueTogether(
            name='municipio',
            unique_together=set([('cidade', 'estado')]),
        ),
    ]
