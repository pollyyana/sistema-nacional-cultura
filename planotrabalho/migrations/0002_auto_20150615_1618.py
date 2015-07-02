# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planotrabalho', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conselhocultural',
            name='ata_regimento_aprovado',
            field=models.FileField(upload_to='regimentos', blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='criacaosistema',
            name='lei_sistema_cultura',
            field=models.FileField(upload_to='leis_sistema_cultura', blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='criacaosistema',
            name='minuta_projeto_lei',
            field=models.FileField(upload_to='minuta_lei', blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='fundocultura',
            name='lei_fundo_cultura',
            field=models.FileField(upload_to='lei_fundo_cultura', blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='orgaogestor',
            name='relatorio_atividade_secretaria',
            field=models.FileField(upload_to='relatorio_atividades', blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='planocultura',
            name='ata_reuniao_aprovacao_plano',
            field=models.FileField(upload_to='ata_aprovacao_plano', blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='planocultura',
            name='ata_votacao_projeto_lei',
            field=models.FileField(upload_to='ata_votacao_lei', blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='planocultura',
            name='lei_plano_cultura',
            field=models.FileField(upload_to='lei_plano_cultura', blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='planocultura',
            name='minuta_preparada',
            field=models.FileField(upload_to='minuta_preparada', blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='planocultura',
            name='relatorio_diretrizes_aprovadas',
            field=models.FileField(upload_to='relatorio_diretrizes', blank=True, max_length=255, null=True),
        ),
    ]
