# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adesao', '0002_auto_20150512_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsavel',
            name='cpf_responsavel',
            field=models.CharField(verbose_name='CPF', max_length=14, unique=True),
        ),
        migrations.AlterField(
            model_name='secretario',
            name='cpf_secretario',
            field=models.CharField(verbose_name='CPF', max_length=14, unique=True),
        ),
    ]
