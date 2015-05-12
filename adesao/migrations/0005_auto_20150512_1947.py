# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adesao', '0004_auto_20150512_1821'),
    ]

    operations = [
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf_prefeito', models.CharField(unique=True, verbose_name='CPF', max_length=14)),
                ('nome_prefeito', models.CharField(max_length=100)),
                ('cnpj_prefeitura', models.CharField(unique=True, verbose_name='CNPJ', max_length=18)),
                ('endereco', models.CharField(max_length=100)),
                ('complemento', models.CharField(max_length=100)),
                ('cep', models.CharField(max_length=9)),
                ('bairro', models.CharField(max_length=50)),
                ('cidade', models.CharField(max_length=50)),
                ('telefone_um', models.CharField(max_length=15)),
                ('telefone_dois', models.CharField(blank=True, max_length=15)),
                ('telefone_tres', models.CharField(blank=True, max_length=15)),
                ('email_institucional_prefeito', models.EmailField(max_length=254)),
                ('estado', models.ForeignKey(to='adesao.Uf')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='prefeitura',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='prefeitura',
            name='estado',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='prefeitura',
            field=models.OneToOneField(null=True, to='adesao.Municipio', blank=True),
        ),
        migrations.DeleteModel(
            name='Prefeitura',
        ),
        migrations.AlterUniqueTogether(
            name='municipio',
            unique_together=set([('cidade', 'estado')]),
        ),
    ]
