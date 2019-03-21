# Generated by Django 2.0.8 on 2019-03-20 19:25

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        ('adesao', '0037_merge_20190320_1154'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gestao', '0008_merge_20181010_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalDiligenciaSimples',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('texto_diligencia', models.TextField(max_length=200)),
                ('classificacao_arquivo', models.IntegerField(blank=True, choices=[(0, 'Em preenchimento'), (1, 'Avaliando anexo'), (2, 'Concluída'), (3, 'Arquivo aprovado com ressalvas'), (4, 'Arquivo danificado'), (5, 'Arquivo incompleto'), (6, 'Arquivo incorreto')], null=True)),
                ('data_criacao', models.DateField(default=datetime.date.today)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='adesao.Usuario')),
            ],
            options={
                'verbose_name': 'historical diligencia simples',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]