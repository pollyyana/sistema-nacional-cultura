from django.contrib import admin

from .models import Municipio, Responsavel, Secretario

# Register your models here.
admin.site.register(Municipio)
admin.site.register(Responsavel)
admin.site.register(Secretario)
