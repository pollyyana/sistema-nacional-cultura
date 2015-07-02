# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adesao', '0006_historico_situacao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Acordo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='EnteAcordo',
            fields=[
                ('municipio_ptr', models.OneToOneField(parent_link=True, serialize=False, to='adesao.Municipio', auto_created=True, primary_key=True)),
            ],
            bases=('adesao.municipio',),
        ),
        migrations.CreateModel(
            name='InterlocutorAcordo',
            fields=[
                ('secretario_ptr', models.OneToOneField(parent_link=True, serialize=False, to='adesao.Secretario', auto_created=True, primary_key=True)),
            ],
            bases=('adesao.secretario',),
        ),
        migrations.CreateModel(
            name='ResponsavelAcordo',
            fields=[
                ('responsavel_ptr', models.OneToOneField(parent_link=True, serialize=False, to='adesao.Responsavel', auto_created=True, primary_key=True)),
            ],
            bases=('adesao.responsavel',),
        ),
        migrations.AddField(
            model_name='acordo',
            name='ente_acordo',
            field=models.ForeignKey(to='adesao.EnteAcordo'),
        ),
        migrations.AddField(
            model_name='acordo',
            name='interlocutor_acordo',
            field=models.ForeignKey(to='adesao.InterlocutorAcordo'),
        ),
        migrations.AddField(
            model_name='acordo',
            name='responsavel_acordo',
            field=models.ForeignKey(to='adesao.ResponsavelAcordo'),
        ),
        migrations.AddField(
            model_name='acordo',
            name='usuario',
            field=models.OneToOneField(to='adesao.Usuario'),
        ),
    ]
