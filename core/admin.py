from django.contrib import admin
from .models import Evento, Documento, Blog, About, Equipo

admin.site.register(Evento)
admin.site.register(Documento)
admin.site.register(Blog)
admin.site.register(About)
admin.site.register(Equipo)