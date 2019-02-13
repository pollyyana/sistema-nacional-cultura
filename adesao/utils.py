import re

from threading import Thread

from django.core.mail import send_mail
from django.forms.models import model_to_dict
from adesao.models import SistemaCultura
from django.core.exceptions import ObjectDoesNotExist


def limpar_mascara(mascara):
    return ''.join(re.findall('\d+', mascara))


def enviar_email_conclusao(user, message_txt, message_html):
    Thread(target=send_mail, args=(
        'Sistema Nacional de Cultura - Solicitação de Adesão ao SNC',
        message_txt,
        'naoresponda@cultura.gov.br',
        [user.email],),
        kwargs = {'fail_silently': 'False', 'html_message': message_html}
        ).start()


def verificar_anexo(sistema, componente):
    try:
        componente = getattr(sistema, componente)
        if componente:
            return componente.get_situacao_display()
        else:
            return 'Não Possui'
    except (AttributeError, ObjectDoesNotExist) as exceptions:
        return 'Não Possui'


def preenche_planilha(planilha):
    planilha.write(0, 0, "Ente Federado")
    planilha.write(0, 1, "Cod.IBGE")
    planilha.write(0, 2, "Situação")
    planilha.write(0, 3, "Situação da Lei do Sistema de Cultura")
    planilha.write(0, 4, "Situação do Órgão Gestor")
    planilha.write(0, 5, "Situação do Conselho de Política Cultural")
    planilha.write(0, 6, "Situação do Fundo de Cultura")
    planilha.write(0, 7, "Situação do Plano de Cultura")
    planilha.write(0, 8, "IDH")
    planilha.write(0, 9, "PIB")
    planilha.write(0, 10, "População")
    planilha.write(0, 11, "Endereço")
    planilha.write(0, 12, "Bairro")
    planilha.write(0, 13, "CEP")
    planilha.write(0, 14, "Telefone")
    planilha.write(0, 15, "Email Prefeito")
    planilha.write(0, 16, "Email do Cadastrador")
    planilha.write(0, 17, "Email do Responsável")
    planilha.write(0, 18, "Localização do processo")
    
    ultima_linha = 0

    for i, sistema in enumerate(SistemaCultura.sistema.all(), start=1):
        if sistema.ente_federado:
            if sistema.ente_federado.is_municipio:
                nome = sistema.ente_federado.__str__()
            else:
                nome = "Estado de " + sistema.ente_federado.nome
            cod_ibge = sistema.ente_federado.cod_ibge
            idh = sistema.ente_federado.idh
            pib = sistema.ente_federado.pib
            populacao = sistema.ente_federado.populacao
        else:
            nome = "Nome não cadastrado"
            cod_ibge = "Código não cadastrado"

        estado_processo = sistema.get_estado_processo_display()

        if sistema.sede:
            endereco = sistema.sede.endereco
            bairro = sistema.sede.bairro
            cep = sistema.sede.cep
            telefone = sistema.sede.telefone_um
        else:
            endereco = "Não cadastrado"
            bairro = "Não cadastrado"
            cep = "Não cadastrado"
            telefone = "Não cadastrado"

        if sistema.gestor:
            email_gestor = sistema.gestor.email_institucional
        else:
            email_gestor = "Não cadastrado"

        if sistema.cadastrador:
            email_cadastrador = sistema.cadastrador.user.email
        else:
            email_cadastrador = "Não cadastrado"

        if sistema.responsavel:
            email_responsavel = sistema.responsavel.email_institucional
        else:
            email_responsavel = "Não cadastrado"

        local = sistema.localizacao

        planilha.write(i, 0, nome)
        planilha.write(i, 1, cod_ibge)
        planilha.write(i, 2, estado_processo)
        planilha.write(i, 3, verificar_anexo(sistema, "legislacao"))
        planilha.write(i, 4, verificar_anexo(sistema, "orgao_gestor"),)
        planilha.write(i, 5, verificar_anexo(sistema, "conselho"),)
        planilha.write(i, 6, verificar_anexo(sistema, "fundo_cultura"))
        planilha.write(i, 7, verificar_anexo(sistema, "plano"))
        planilha.write(i, 8, idh)
        planilha.write(i, 9, pib)
        planilha.write(i, 10, populacao)
        planilha.write(i, 11, endereco)
        planilha.write(i, 12, bairro)
        planilha.write(i, 13, cep)
        planilha.write(i, 14, telefone)
        planilha.write(i, 15, email_gestor)
        planilha.write(i, 16, email_cadastrador)
        planilha.write(i, 17, email_responsavel)
        planilha.write(i, 18, local)
        
        ultima_linha = i

    return ultima_linha


def atualiza_session(sistema_cultura, request):
    request.session['sistema_cultura_selecionado'] = model_to_dict(sistema_cultura, exclude=['data_criacao', 'alterado_em',
        'data_publicacao_acordo'])
    request.session['sistema_situacao'] = sistema_cultura.get_estado_processo_display()
    request.session['sistema_sede'] = model_to_dict(sistema_cultura.sede)
    request.session['sistema_gestor'] = model_to_dict(sistema_cultura.gestor, exclude=['termo_posse', 'rg_copia', 'cpf_copia'])
    request.session['sistema_ente'] = model_to_dict(sistema_cultura.ente_federado, fields=['nome', 'cod_ibge'])

    if sistema_cultura.responsavel:
        request.session['sistema_responsavel'] = model_to_dict(sistema_cultura.responsavel)
    else:
        if request.session.get('sistema_responsavel', False):
            request.session['sistema_responsavel'].clear()

    if sistema_cultura.secretario:
        request.session['sistema_secretario'] = model_to_dict(sistema_cultura.secretario)
    else:
        if request.session.get('sistema_secretario', False):
            request.session['sistema_secretario'].clear()

    request.session.modified = True