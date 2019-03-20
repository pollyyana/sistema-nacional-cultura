# Generated by Django 2.0.8 on 2019-03-15 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planotrabalho', '0021_auto_20190311_1058'),
    ]

    operations = [
        migrations.RunSQL(
            'ALTER TABLE \
            planotrabalho_conselheiro \
            ADD CONSTRAINT planotrabalho_consel_conselho_id_8690ac4f_fk_planotrab \
            FOREIGN KEY (conselho_id) \
            REFERENCES planotrabalho_componente(arquivocomponente2_ptr_id) \
            DEFERRABLE INITIALLY DEFERRED'
        ),
    ]