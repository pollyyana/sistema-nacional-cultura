# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adesao', '0007_auto_20150702_1358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acordo',
            name='ente_acordo',
        ),
        migrations.RemoveField(
            model_name='acordo',
            name='interlocutor_acordo',
        ),
        migrations.RemoveField(
            model_name='acordo',
            name='responsavel_acordo',
        ),
        migrations.RemoveField(
            model_name='acordo',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='enteacordo',
            name='municipio_ptr',
        ),
        migrations.RemoveField(
            model_name='interlocutoracordo',
            name='secretario_ptr',
        ),
        migrations.RemoveField(
            model_name='responsavelacordo',
            name='responsavel_ptr',
        ),
        migrations.DeleteModel(
            name='Acordo',
        ),
        migrations.DeleteModel(
            name='EnteAcordo',
        ),
        migrations.DeleteModel(
            name='InterlocutorAcordo',
        ),
        migrations.DeleteModel(
            name='ResponsavelAcordo',
        ),
    ]
