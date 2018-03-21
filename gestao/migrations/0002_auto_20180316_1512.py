# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diligencia',
            name='classificacao_arquivo',
            field=models.ForeignKey(blank=True, to='planotrabalho.SituacoesArquivoPlano', null=True),
        ),
        migrations.AlterField(
            model_name='diligencia',
            name='tipo_diligencia',
            field=models.CharField(max_length=10, choices=[('geral', 'Geral do plano de trabalho'), ('componente', 'Específica de um componente')]),
        ),
    ]
