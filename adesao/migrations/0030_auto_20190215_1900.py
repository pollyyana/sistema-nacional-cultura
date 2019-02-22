# Generated by Django 2.0.8 on 2019-02-15 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planotrabalho', '0014_auto_20190208_1733'),
        ('adesao', '0032_merge_20190221_1414'),
    ]

    def copia_fks(apps, schema_editor):
        SistemaCultura = apps.get_model('adesao', 'SistemaCultura')
        Componente = apps.get_model('planotrabalho', 'Componente')
        Componente2 = apps.get_model('planotrabalho', 'Componente2')
        FundoDeCultura2 = apps.get_model('planotrabalho', 'FundoDeCultura2')

        componentes = ('legislacao', 'orgao_gestor',
                       'fundo_cultura', 'conselho', 'plano')

        for sistema in SistemaCultura.objects.all():
            for componente in componentes:
                if not getattr(sistema, componente):
                    continue

                old_componente = getattr(sistema, componente)

                if componente != 'fundo_cultura':
                    new_componente = Componente2.objects.get(id=old_componente.id)
                else:
                    new_componente = FundoDeCultura2.objects.get(id=old_componente.id)

                setattr(sistema, componente+'2', new_componente)
            sistema.save()

    operations = [
        migrations.AddField(
            model_name='sistemacultura',
            name='conselho2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='conselho', to='planotrabalho.Componente2'),
        ),
        migrations.AddField(
            model_name='sistemacultura',
            name='fundo_cultura2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fundo_cultura', to='planotrabalho.FundoDeCultura2'),
        ),
        migrations.AddField(
            model_name='sistemacultura',
            name='legislacao2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='legislacao', to='planotrabalho.Componente2'),
        ),
        migrations.AddField(
            model_name='sistemacultura',
            name='orgao_gestor2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orgao_gestor', to='planotrabalho.Componente2'),
        ),
        migrations.AddField(
            model_name='sistemacultura',
            name='plano2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='plano', to='planotrabalho.Componente2'),
        ),
        migrations.RunPython(copia_fks, migrations.RunPython.noop),
    ]
