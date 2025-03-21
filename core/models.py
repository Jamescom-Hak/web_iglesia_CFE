from django.db import models

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    descripcion = models.TextField()
    es_oracion = models.BooleanField(default=False)
    nombre_imagen = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.titulo
    
class Documento(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    archivo = models.FileField(upload_to='descargas/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
class Blog(models.Model):
    titulo = models.CharField(max_length=100)
    introduccion = models.TextField()  # Para la vista previa en Home
    contenido = models.TextField()     # Contenido completo
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    nombre_imagen = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.titulo
    
class About(models.Model):
    remembranza = models.TextField()
    historia = models.TextField()
    mision = models.TextField()
    vision = models.TextField()

    def __str__(self):
        return "Información Acerca de"

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=100)
    nombre_imagen = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.nombre
    