""" 
Carga de las diferentes instancias para el correcto funcionamiento de la App
"""
from django.contrib import admin
from core.models import Evento, Documento, Blog, About, Equipo


class BlogAdmin(admin.ModelAdmin):
    """  
    Esta clase es necesaria para visualizar el campo de fecha de publicación
    y se pueda visualizar en la BD por medio del Admin
    """
    # Campos que se mostrarán en el formulario del administrador
    list_display = ('titulo', 'fecha_publicacion')  # Muestra el título y la fecha de publicación
    readonly_fields = ('fecha_publicacion',)       # Hace que el campo sea de solo lectura


admin.site.register(Evento)
admin.site.register(Documento)
admin.site.register(Blog, BlogAdmin)
admin.site.register(About)
admin.site.register(Equipo)
