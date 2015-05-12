# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adesao', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prefeitura',
            name='cnpj_prefeitura',
            field=models.CharField(verbose_name='CNPJ', unique=True, max_length=18),
        ),
        migrations.AlterField(
            model_name='prefeitura',
            name='cpf_prefeito',
            field=models.CharField(verbose_name='CPF', unique=True, max_length=14),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='email_usuario',
            field=models.EmailField(unique=True, max_length=254),
        ),
    ]
