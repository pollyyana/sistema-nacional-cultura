# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conselheiro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('segmento', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('situacao', models.CharField(default=1, blank=True, choices=[('1', 'Habilitado'), ('0', 'Desabilitado')], max_length=1, null=True)),
                ('data_cadastro', models.DateField(null=True, blank=True)),
                ('data_situacao', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConselhoCultural',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('ata_regimento_aprovado', models.FileField(null=True, upload_to='regimentos', max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CriacaoSistema',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('minuta_projeto_lei', models.FileField(null=True, upload_to='minuta_lei', max_length=255, blank=True)),
                ('lei_sistema_cultura', models.FileField(null=True, upload_to='leis_sistema_cultura', max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FundoCultura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('cnpj_fundo_cultura', models.CharField(verbose_name='CNPJ', default=None, blank=True, max_length=18, null=True)),
                ('lei_fundo_cultura', models.FileField(null=True, upload_to='lei_fundo_cultura', max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrgaoGestor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('relatorio_atividade_secretaria', models.FileField(null=True, upload_to='relatorio_atividades', max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlanoCultura',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('relatorio_diretrizes_aprovadas', models.FileField(null=True, upload_to='relatorio_diretrizes', max_length=255, blank=True)),
                ('minuta_preparada', models.FileField(null=True, upload_to='minuta_preparada', max_length=255, blank=True)),
                ('ata_reuniao_aprovacao_plano', models.FileField(null=True, upload_to='ata_aprovacao_plano', max_length=255, blank=True)),
                ('ata_votacao_projeto_lei', models.FileField(null=True, upload_to='ata_votacao_lei', max_length=255, blank=True)),
                ('lei_plano_cultura', models.FileField(null=True, upload_to='lei_plano_cultura', max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlanoTrabalho',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('conselho_cultural', models.OneToOneField(null=True, to='planotrabalho.ConselhoCultural', blank=True)),
                ('criacao_sistema', models.OneToOneField(null=True, to='planotrabalho.CriacaoSistema', blank=True)),
                ('fundo_cultura', models.OneToOneField(null=True, to='planotrabalho.FundoCultura', blank=True)),
                ('orgao_gestor', models.OneToOneField(null=True, to='planotrabalho.OrgaoGestor', blank=True)),
                ('plano_cultura', models.OneToOneField(null=True, to='planotrabalho.PlanoCultura', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SituacoesArquivoPlano',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('descricao', models.CharField(max_length=75)),
            ],
        ),
        migrations.AddField(
            model_name='planocultura',
            name='situacao_lei_plano',
            field=models.ForeignKey(to='planotrabalho.SituacoesArquivoPlano'),
        ),
        migrations.AddField(
            model_name='orgaogestor',
            name='situacao_relatorio_secretaria',
            field=models.ForeignKey(to='planotrabalho.SituacoesArquivoPlano'),
        ),
        migrations.AddField(
            model_name='fundocultura',
            name='situacao_lei_plano',
            field=models.ForeignKey(to='planotrabalho.SituacoesArquivoPlano'),
        ),
        migrations.AddField(
            model_name='criacaosistema',
            name='situacao_lei_sistema',
            field=models.ForeignKey(to='planotrabalho.SituacoesArquivoPlano'),
        ),
        migrations.AddField(
            model_name='conselhocultural',
            name='situacao_ata',
            field=models.ForeignKey(to='planotrabalho.SituacoesArquivoPlano'),
        ),
        migrations.AddField(
            model_name='conselheiro',
            name='conselho',
            field=models.ForeignKey(to='planotrabalho.ConselhoCultural'),
        ),
    ]
