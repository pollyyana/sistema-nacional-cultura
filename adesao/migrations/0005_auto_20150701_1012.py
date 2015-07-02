# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adesao', '0004_auto_20150701_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historico',
            name='usuario',
            field=models.ForeignKey(to='adesao.Usuario'),
        ),
    ]
