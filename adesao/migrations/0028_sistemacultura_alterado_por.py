# Generated by Django 2.0.8 on 2019-01-25 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adesao', '0027_auto_20190124_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='sistemacultura',
            name='alterado_por',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sistemas_alterados', to='adesao.Usuario'),
        ),
    ]