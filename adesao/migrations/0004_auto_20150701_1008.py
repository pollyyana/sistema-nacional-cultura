# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adesao', '0003_auto_20150616_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historico',
            name='usuario',
            field=models.OneToOneField(to='adesao.Usuario'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='estado_processo',
            field=models.CharField(max_length=1, choices=[('0', 'Aguardando preenchimento dos dados cadastrais'), ('1', 'Aguardando envio da documentação'), ('2', 'Documentação Recebida - Aguarda Análise'), ('3', 'Diligência Documental'), ('4', 'Encaminhado para assinatura do Secretário SAI'), ('5', 'Aguarda Publicação no DOU'), ('6', 'Publicado no DOU'), ('7', 'Responsável confirmado')], default='0'),
        ),
    ]
