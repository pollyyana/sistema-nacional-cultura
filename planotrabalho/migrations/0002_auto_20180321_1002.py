# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import planotrabalho.models


class Migration(migrations.Migration):

    dependencies = [
        ('planotrabalho', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conselhocultural',
            name='arquivo',
            field=models.FileField(upload_to=planotrabalho.models.upload_to_componente, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='conselhocultural',
            name='data_envio',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='conselhocultural',
            name='situacao',
            field=models.ForeignKey(default=0, to='planotrabalho.SituacoesArquivoPlano', related_name='conselhocultural_situacao'),
        ),
        migrations.AddField(
            model_name='criacaosistema',
            name='arquivo',
            field=models.FileField(upload_to=planotrabalho.models.upload_to_componente, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='criacaosistema',
            name='data_envio',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='criacaosistema',
            name='situacao',
            field=models.ForeignKey(default=0, to='planotrabalho.SituacoesArquivoPlano', related_name='criacaosistema_situacao'),
        ),
        migrations.AddField(
            model_name='fundocultura',
            name='arquivo',
            field=models.FileField(upload_to=planotrabalho.models.upload_to_componente, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='fundocultura',
            name='data_envio',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='fundocultura',
            name='situacao',
            field=models.ForeignKey(default=0, to='planotrabalho.SituacoesArquivoPlano', related_name='fundocultura_situacao'),
        ),
        migrations.AddField(
            model_name='orgaogestor',
            name='arquivo',
            field=models.FileField(upload_to=planotrabalho.models.upload_to_componente, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='orgaogestor',
            name='data_envio',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='orgaogestor',
            name='situacao',
            field=models.ForeignKey(default=0, to='planotrabalho.SituacoesArquivoPlano', related_name='orgaogestor_situacao'),
        ),
        migrations.AddField(
            model_name='planocultura',
            name='arquivo',
            field=models.FileField(upload_to=planotrabalho.models.upload_to_componente, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='planocultura',
            name='data_envio',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='planocultura',
            name='situacao',
            field=models.ForeignKey(default=0, to='planotrabalho.SituacoesArquivoPlano', related_name='planocultura_situacao'),
        ),
    ]
