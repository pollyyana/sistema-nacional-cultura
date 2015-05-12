# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adesao', '0003_auto_20150512_1747'),
    ]

    operations = [
        migrations.RenameField(
            model_name='secretario',
            old_name='instituicao_responsavel',
            new_name='instituicao_secretario',
        ),
    ]
