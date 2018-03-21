# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('planotrabalho', '__first__'),
        ('adesao', '__first__'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diligencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('texto_diligencia', models.TextField(max_length=200)),
                ('data_criacao', models.DateField(default=datetime.date.today)),
                ('componente_id', models.PositiveIntegerField()),
                ('tipo_diligencia', models.TextField(max_length=12)),
                ('classificacao_arquivo', models.ForeignKey(to='planotrabalho.SituacoesArquivoPlano')),
                ('componente_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('ente_federado', models.ForeignKey(to='adesao.Municipio')),
                ('usuario', models.ForeignKey(to='adesao.Usuario')),
            ],
        ),
    ]
