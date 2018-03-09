# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('planotrabalho', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cidade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('codigo_ibge', models.IntegerField(unique=True)),
                ('nome_municipio', models.CharField(max_length=100)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
            ],
            options={
                'ordering': ['nome_municipio'],
            },
        ),
        migrations.CreateModel(
            name='Historico',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('situacao', models.CharField(null=True, choices=[('0', 'Aguardando preenchimento dos dados cadastrais'), ('1', 'Aguardando envio da documentação'), ('2', 'Documentação Recebida - Aguarda Análise'), ('3', 'Diligência Documental'), ('4', 'Encaminhado para assinatura do Secretário SAI'), ('5', 'Aguarda Publicação no DOU'), ('6', 'Publicado no DOU'), ('7', 'Responsável confirmado')], max_length=1, blank=True)),
                ('data_alteracao', models.DateTimeField(auto_now_add=True)),
                ('arquivo', models.FileField(null=True, upload_to='historico', blank=True)),
                ('descricao', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('localizacao', models.CharField(blank=True, max_length=50)),
                ('numero_processo', models.CharField(blank=True, max_length=50)),
                ('cpf_prefeito', models.CharField(verbose_name='CPF', max_length=14)),
                ('nome_prefeito', models.CharField(max_length=255)),
                ('cnpj_prefeitura', models.CharField(verbose_name='CNPJ', max_length=18)),
                ('rg_prefeito', models.CharField(verbose_name='RG', max_length=50)),
                ('orgao_expeditor_rg', models.CharField(max_length=50)),
                ('endereco', models.CharField(max_length=255)),
                ('complemento', models.CharField(max_length=255)),
                ('cep', models.CharField(max_length=10)),
                ('bairro', models.CharField(max_length=50)),
                ('telefone_um', models.CharField(max_length=100)),
                ('telefone_dois', models.CharField(blank=True, max_length=25)),
                ('telefone_tres', models.CharField(blank=True, max_length=25)),
                ('endereco_eletronico', models.URLField(null=True, max_length=255, blank=True)),
                ('email_institucional_prefeito', models.EmailField(max_length=254)),
                ('termo_posse_prefeito', models.FileField(null=True, upload_to='termo_posse', max_length=255, blank=True)),
                ('rg_copia_prefeito', models.FileField(null=True, upload_to='rg_copia', max_length=255, blank=True)),
                ('cpf_copia_prefeito', models.FileField(null=True, upload_to='cpf_copia', max_length=255, blank=True)),
                ('cidade', smart_selects.db_fields.ChainedForeignKey(chained_field='estado', null=True, chained_model_field='uf', blank=True, to='adesao.Cidade')),
            ],
        ),
        migrations.CreateModel(
            name='Responsavel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('cpf_responsavel', models.CharField(verbose_name='CPF', max_length=14)),
                ('rg_responsavel', models.CharField(verbose_name='RG', max_length=25)),
                ('orgao_expeditor_rg', models.CharField(max_length=50)),
                ('nome_responsavel', models.CharField(max_length=100)),
                ('cargo_responsavel', models.CharField(max_length=100)),
                ('instituicao_responsavel', models.CharField(max_length=100)),
                ('telefone_um', models.CharField(max_length=25)),
                ('telefone_dois', models.CharField(blank=True, max_length=25)),
                ('telefone_tres', models.CharField(blank=True, max_length=25)),
                ('email_institucional_responsavel', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Secretario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('cpf_secretario', models.CharField(verbose_name='CPF', max_length=14)),
                ('rg_secretario', models.CharField(verbose_name='RG', max_length=25)),
                ('orgao_expeditor_rg', models.CharField(max_length=50)),
                ('nome_secretario', models.CharField(max_length=100)),
                ('cargo_secretario', models.CharField(max_length=100)),
                ('instituicao_secretario', models.CharField(max_length=100)),
                ('telefone_um', models.CharField(max_length=25)),
                ('telefone_dois', models.CharField(blank=True, max_length=25)),
                ('telefone_tres', models.CharField(blank=True, max_length=25)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('nome_usuario', models.CharField(max_length=100)),
                ('estado_processo', models.CharField(default='0', choices=[('0', 'Aguardando preenchimento dos dados cadastrais'), ('1', 'Aguardando envio da documentação'), ('2', 'Documentação Recebida - Aguarda Análise'), ('3', 'Diligência Documental'), ('4', 'Encaminhado para assinatura do Secretário SAI'), ('5', 'Aguarda Publicação no DOU'), ('6', 'Publicado no DOU'), ('7', 'Responsável confirmado')], max_length=1)),
                ('data_publicacao_acordo', models.DateField(null=True, blank=True)),
                ('codigo_ativacao', models.CharField(unique=True, max_length=12)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('prazo', models.IntegerField(default=2)),
                ('municipio', models.OneToOneField(null=True, to='adesao.Municipio', blank=True)),
                ('plano_trabalho', models.OneToOneField(null=True, to='planotrabalho.PlanoTrabalho', blank=True)),
                ('responsavel', models.OneToOneField(null=True, to='adesao.Responsavel', blank=True)),
                ('secretario', models.OneToOneField(null=True, to='adesao.Secretario', blank=True)),
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
            model_name='historico',
            name='usuario',
            field=models.ForeignKey(to='adesao.Usuario'),
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
