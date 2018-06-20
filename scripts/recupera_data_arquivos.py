from os import stat

from datetime import datetime

from planotrabalho.models import PlanoTrabalho

planos = PlanoTrabalho.objects.filter(plano_cultura__isnull=False).prefetch_related()

componentes = ('criacao_sistema', 'orgao_gestor', 'conselho_cultural',
               'fundo_cultura', 'plano_cultura')

for plano in planos:
    for componente in componentes:
        try:
            c = getattr(plano, componente)
            arquivo = c.arquivo.file
            stats = stat(str(arquivo))
            data = datetime.fromtimestamp(stats.st_mtime)
            c.data_envio = data
            c.save()
        except:
            pass
