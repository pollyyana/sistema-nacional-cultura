import re

from threading import Thread

from django.core.mail import send_mail


def validar_cpf(cpf):
    digitos = [int(c) for c in cpf if c.isdigit()]
    if len(digitos) == 11:
        a, b, c, d, e, f, g, h, i, j, k = digitos
        numeros = [a, b, c, d, e, f, g, h, i]
        r = range(10, 1, -1)
        soma = sum([x * y for x, y in zip(numeros, r)])
        resto = soma % 11
        dv1 = (11 - resto if 11 - resto < 10 else 0)
        numeros = [a, b, c, d, e, f, g, h, i, dv1]
        r = range(11, 1, -1)
        soma = sum([x*y for x, y in zip(numeros, r)])
        resto = soma % 11
        dv2 = (11 - resto if 11 - resto < 10 else 0)
        return dv1 == j and dv2 == k
    return False


def validar_cnpj(cnpj):
    """
    Valida CNPJs, retornando apenas a string de números válida.

    # CNPJs errados
    >>> validar_cnpj('abcdefghijklmn')
    False
    >>> validar_cnpj('123')
    False
    >>> validar_cnpj('')
    False
    >>> validar_cnpj(None)
    False
    >>> validar_cnpj('12345678901234')
    False
    >>> validar_cnpj('11222333000100')
    False

    # CNPJs corretos
    >>> validar_cnpj('11222333000181')
    '11222333000181'
    >>> validar_cnpj('11.222.333/0001-81')
    '11222333000181'
    >>> validar_cnpj('  11 222 333 0001 81  ')
    '11222333000181'
    """

    cnpj = ''.join(re.findall('\d', str(cnpj)))

    if (not cnpj) or (len(cnpj) < 14):
        return False

    inteiros = list(map(int, cnpj))
    novo = inteiros[:12]

    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    while len(novo) < 14:
        r = sum([x*y for (x, y) in zip(novo, prod)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)
        prod.insert(0, 6)

    if novo == inteiros:
        return cnpj
    return False


def limpar_mascara(mascara):
    return ''.join(re.findall('\d+', mascara))


def enviar_email_conclusao(user, message):
    Thread(target=send_mail, args=(
        'Sistema Nacional de Cultura - Solicitação de Adesão ao SNC',
        #user.usuario.municipio.cidade+'/'+user.usuario.municipio.estado+',\n' +
        #'Sua Solicitação de Adesão ao Sistema Nacional de Cultura foi ' +
        #'recebida em nosso sistema. Para efetivar seu processo de adesão ' +
        #'é necessário o envio dos documentos listados abaixo, devidamente ' +
        #'assinados pelo(a) Sr(a). '+user.usuario.municipio.nome_prefeito+'\n' +
        #'\nDocumentos:\n\n' +
        #'- 1 (uma) via do formulário de Solicitação de Integração ao SNC\n' +
        #'- 2 (duas) vias do Acordo de Cooperação Federativa\n\n' +
        #'Os documentos devem ser enviados à SAI/MinC pelos correios para ' +
        #'o seguinte endereço:\n\n' +
        #'\tSCS 09, Lote "C", Torre "B", 11º andar - ' +
        #'Ed. Parque Cidade Corporate CEP: 70308-200 - Brasília/DF\n\n' +
        #'Seu prazo para o envio é de até 60 dias corridos.\n\n' +
        #'Atenciosamente,\n\nEquipe SNC',
        message,
        'naoresponda@cultura.gov.br',
        [user.email],),
        kwargs = {'fail_silently': 'False', }
    ).start()
