# Generated by Django 2.0.8 on 2019-01-14 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adesao', '0024_auto_20181130_1730'),
        ('adesao', '0028_auto_20190116_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='link_publicacao_acordo',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]