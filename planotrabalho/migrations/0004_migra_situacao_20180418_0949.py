# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migra_situacao_sistema(apps, schema_editor):
    """ Migra situação do Componente do
    field situacao_lei_sistema para situacao """

    CriacaoSistema = apps.get_model("planotrabalho", "CriacaoSistema")
    for sistema in CriacaoSistema.objects.all():
        if sistema.situacao_lei_sistema_id:
            sistema.situacao_id = sistema.situacao_lei_sistema_id
            sistema.save()


def migra_situacao_orgao(apps, schema_editor):
    """ Migra situacao do Componente do field
    situacao_relatorio_secretaria para situacao """

    OrgaoGestor = apps.get_model("planotrabalho", "OrgaoGestor")
    for orgao in OrgaoGestor.objects.all():
        if orgao.situacao_relatorio_secretaria_id:
            orgao.situacao_id = orgao.situacao_relatorio_secretaria_id
            orgao.save()


def migra_situacao_conselho(apps, schema_editor):
    """ Migra situacao do Componente do field
    situacao_ata para situacao """

    ConselhoCultural = apps.get_model("planotrabalho", "ConselhoCultural")
    for conselho in ConselhoCultural.objects.all():
        if conselho.situacao_ata_id:
            conselho.situacao_id = conselho.situacao_ata_id
            conselho.save()


def migra_situacao_fundo(apps, schema_editor):
    """ Migra situacao do Componente do field
    situacao_lei_plano para situacao """

    FundoCultura = apps.get_model("planotrabalho", "FundoCultura")
    for fundo in FundoCultura.objects.all():
        if fundo.situacao_lei_plano_id:
            fundo.situacao_id = fundo.situacao_lei_plano_id
            fundo.save()


def migra_situacao_plano(apps, schema_editor):
    """ Migra situacao do Componente do field
    situacao_lei_plano para situacao """

    PlanoCultura = apps.get_model("planotrabalho", "PlanoCultura")
    for plano in PlanoCultura.objects.all():
        if plano.situacao_lei_plano_id:
            plano.situacao_id = plano.situacao_lei_plano_id
            plano.save()


class Migration(migrations.Migration):

    dependencies = [
        ('planotrabalho', '0003_recupera_data_envio_arquivos'),
    ]

    operations = [
        migrations.RunPython(migra_situacao_sistema),
        migrations.RunPython(migra_situacao_orgao),
        migrations.RunPython(migra_situacao_conselho),
        migrations.RunPython(migra_situacao_fundo),
        migrations.RunPython(migra_situacao_plano),
    ]
