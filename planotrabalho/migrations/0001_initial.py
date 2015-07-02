# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConselhoCultural',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('data_final_instalacao_conselho', models.DateField()),
                ('ata_regimento_aprovado', models.FileField(null=True, upload_to='regimentos', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CriacaoSistema',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('data_final_elaboracao_projeto_lei', models.DateField()),
                ('minuta_projeto_lei', models.FileField(null=True, upload_to='minuta_lei', blank=True)),
                ('data_final_sancao_lei', models.DateField()),
                ('lei_sistema_cultura', models.FileField(null=True, upload_to='leis_sistema_cultura', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FundoCultura',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('data_final_instituicao_fundo_cultura', models.DateField()),
                ('cnpj_fundo_cultura', models.CharField(max_length=18, verbose_name='CNPJ', null=True, blank=True, unique=True)),
                ('lei_fundo_cultura', models.FileField(null=True, upload_to='lei_fundo_cultura', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrgaoGestor',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('data_final_estruturacao_secretaria', models.DateField()),
                ('relatorio_atividade_secretaria', models.FileField(null=True, upload_to='relatorio_atividades', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlanoCultura',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('data_final_estabelecimento_instancias', models.DateField()),
                ('relatorio_diretrizes_aprovadas', models.FileField(null=True, upload_to='relatorio_diretrizes', blank=True)),
                ('data_final_elaboracao_plano_cultura', models.DateField()),
                ('minuta_preparada', models.FileField(null=True, upload_to='minuta_preparada', blank=True)),
                ('data_final_aprovacao_plano_cultura', models.DateField()),
                ('ata_reuniao_aprovacao_plano', models.FileField(null=True, upload_to='ata_aprovacao_plano', blank=True)),
                ('data_final_tramitacao_projeto_lei', models.DateField()),
                ('ata_votacao_projeto_lei', models.FileField(null=True, upload_to='ata_votacao_lei', blank=True)),
                ('data_final_sancao_lei_plano_cultura', models.DateField()),
                ('lei_plano_cultura', models.FileField(null=True, upload_to='lei_plano_cultura', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlanoTrabalho',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('conselho_cultural', models.OneToOneField(blank=True, null=True, to='planotrabalho.ConselhoCultural')),
                ('criacao_sistema', models.OneToOneField(blank=True, null=True, to='planotrabalho.CriacaoSistema')),
                ('fundo_cultura', models.OneToOneField(blank=True, null=True, to='planotrabalho.FundoCultura')),
                ('orgao_gestor', models.OneToOneField(blank=True, null=True, to='planotrabalho.OrgaoGestor')),
                ('plano_cultura', models.OneToOneField(blank=True, null=True, to='planotrabalho.PlanoCultura')),
            ],
        ),
    ]
