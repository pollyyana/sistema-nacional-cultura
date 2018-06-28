# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestao', '0002_auto_20180316_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diligencia',
            name='tipo_diligencia',
            field=models.CharField(choices=[('geral', 'Geral'), ('componente', 'Específica')], max_length=10),
        ),
    ]
