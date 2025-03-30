""" 
Carga de las diferentes instancias para el correcto funcionamiento de la App
"""
from django.db import models


class Evento(models.Model):
    """  
    Informaciòn sobre los diferentes eventos relacionados por la iglesia
    """
    titulo = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    descripcion = models.TextField()
    es_oracion = models.BooleanField(default=False)
    nombre_imagen = models.CharField(max_length=30, default='')

    # Definir el administrador de objetos
    objects = models.Manager()

    def __str__(self):
        return str(self.titulo)


class Documento(models.Model):
    """  
    Documentos relacionados en la pantalla de downloads
    """
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    archivo = models.FileField(upload_to='descargas/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    # Definir el administrador de objetos
    objects = models.Manager()

    def __str__(self):
        return str(self.titulo)


class Blog(models.Model):
    """ 
    Informaciòn relacionada a los diferentes blogs establecidos por la 
    iglesia y presentados en la pantalla de Blogs
    """
    titulo = models.CharField(max_length=100)
    introduccion = models.TextField()  # Para la vista previa en Home
    contenido = models.TextField()     # Contenido completo
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    nombre_imagen = models.CharField(max_length=30, default='')

    # Definir el administrador de objetos
    objects = models.Manager()

    def __str__(self):
        return str(self.titulo)


class About(models.Model):
    """ 
    Informacìon de la iglesia para ser mostrada en la pantalla Acerca de 
    """
    remembranza = models.TextField()
    historia = models.TextField()
    mision = models.TextField()
    vision = models.TextField()

    # Definir el administrador de objetos
    objects = models.Manager()

    def __str__(self):
        return "Información Acerca de"


class Equipo(models.Model):
    """ 
    Modelo Implementado para identificar ante la iglesia los diferentes 
    servidores vigentes
    """
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=100)
    nombre_imagen = models.CharField(max_length=30, default='')

    # Definir el administrador de objetos
    objects = models.Manager()

    def __str__(self):
        return str(self.nombre)
