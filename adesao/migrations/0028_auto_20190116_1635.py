# Generated by Django 2.0.8 on 2019-01-16 18:35

from django.db import migrations
from django.core.exceptions import ObjectDoesNotExist


def migra_prazo(apps, schema_editor):

	SistemaCultura = apps.get_model('adesao', 'SistemaCultura')
	Municipio = apps.get_model('adesao', 'Municipio')
	Cidade = apps.get_model('adesao', 'Cidade')

	for municipio in Municipio.objects.all():

		try:
			if municipio.usuario:
				if municipio.cidade is None:
					sistema_cultura = SistemaCultura.objects.filter(
						ente_federado__cod_ibge=municipio.estado.codigo_ibge).distinct('ente_federado')

					if not sistema_cultura or len(sistema_cultura) > 1:
						sistema_cultura = SistemaCultura.objects.filter(
							ente_federado__nome__icontains=municipio.estado.nome_uf).distinct('ente_federado')
				else:
					cidade = Cidade.objects.get(nome_municipio=municipio.cidade.nome_municipio, uf=municipio.estado)
					sistema_cultura = SistemaCultura.objects.filter(ente_federado__cod_ibge=cidade.codigo_ibge).distinct('ente_federado')

					if not sistema_cultura or len(sistema_cultura) > 1:
						sistema_cultura = SistemaCultura.objects.filter(
							ente_federado__cod_ibge__startswith=cidade.codigo_ibge).distinct('ente_federado')

				sistema_cultura = sistema_cultura[0]

				sistema_cultura.prazo = municipio.usuario.prazo
				sistema_cultura.save()

		except ObjectDoesNotExist:
			pass


class Migration(migrations.Migration):

    dependencies = [
    	('adesao', '0027_sistemacultura_prazo'),
        ('adesao', '0024_auto_20181130_1730'),
    ]

    operations = [
    	migrations.RunPython(migra_prazo),
    ]