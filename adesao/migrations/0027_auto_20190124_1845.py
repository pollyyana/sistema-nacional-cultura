# Generated by Django 2.0.8 on 2019-01-24 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adesao', '0026_merge_20190115_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sistemacultura',
            name='link_publicacao_acordo',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]