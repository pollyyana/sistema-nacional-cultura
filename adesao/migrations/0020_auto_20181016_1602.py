# Generated by Django 2.0.8 on 2018-10-16 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adesao', '0019_auto_20181005_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='sistemacultura',
            name='justificativa',
            field=models.TextField(blank=True, null=True, verbose_name='Justificativa'),
        ),
        migrations.AddField(
            model_name='sistemacultura',
            name='localizacao',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Localização do Processo'),
        ),
    ]
