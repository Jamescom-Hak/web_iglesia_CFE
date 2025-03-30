# core/views.py
""" 
Recarga de las diferentes estancias necesarias para el funcionamiento 
de la App 
"""
from django.utils import timezone
from django.shortcuts import render
from core.models import About, Equipo, Evento, Documento, Blog


def home(request):
    """ 
    En Home tenemos las opciones principales para el usuario, 
    en ella por medio de bloques el usuario se entera de los principales 
    acontecimientos de la iglesi y por medio de links puede acceder a 
    la informaciòn respectiva
    """
    eventos_destacados = Evento.objects.order_by('-fecha')[:3]
    ultimo_blog = Blog.objects.order_by('-fecha_publicacion').first()
    evento_especifico = Evento.objects.get(id=1)  # Cambia el ID por el de tu evento
    return render(request, 'home.html', {
        'eventos': eventos_destacados,
        'ultimo_blog': ultimo_blog,
        'evento_especifico': evento_especifico,
    })


def about(request):
    """ 
    Pantalla para informar acerca de la organizaciòn en este caso 
    la iglesia 
    """
    about_info = About.objects.first()  # Tomamos el primer registro (solo habrá uno)
    equipo = Equipo.objects.all()
    context = {
        'about': about_info,
        'equipo': equipo
    }
    return render(request, 'about.html', context)


def events(request):
    """
      Pantalla cuyo objetivo es dar informaciòn detallada sobre los diferentes
      eventos programados para la iglesia
    """
    eventos = Evento.objects.order_by('-fecha')
    return render(request, 'events.html', {'eventos': eventos})


def resources(request):
    """ 
    Recursos documentales o audivisuales para promover la enseñanza de 
    la palabra de Dios, de los diferentes ministerios o para cumplimiento 
    de actividdes como el bautismo, etc.
    """
    recursos = [
        {'titulo': 'Sermón: La Gracia de Dios', 'tipo': 'Audio', 'url': '#'},
        {'titulo': 'Devocional Semanal', 'tipo': 'PDF', 'url': '#'},
    ]
    return render(request, 'resources.html', {'recursos': recursos})


def contact(request):
    """ 
    Lugar donde el usuario puede ver las diferentes formas de contacto 
    con la iglesia, asì mismo por medio de un formulario puede enviar 
    un mensaje directo al email oficial de la iglesia
    """
    context = {
        'ubicacion': 'Calle Ejemplo 123, Ciudad, País',
        'email': 'contacto@iglesia.com',
        'telefono': '+123 456 7890',
    }
    return render(request, 'contact.html', context)


def prayer_meetings(request):
    """ 
    Pantalla donde el usuario puede consultar los diferentes enciuentros 
    de Oraciòn programados para el año vigente 
    """
    current_year = timezone.now().year
    # Último encuentro realizado (fecha pasada, es_oracion=True)
    ultimo_encuentro = Evento.objects.filter(
        es_oracion=True,
        fecha__lt=timezone.now()
    ).order_by('-fecha').first()  # El más reciente

    # Próximos encuentros del año actual (fecha futura, es_oracion=True)
    proximos_encuentros = Evento.objects.filter(
        es_oracion=True,
        fecha__gte=timezone.now(),
        fecha__year=current_year
    ).order_by('fecha')

    context = {
        'ultimo_encuentro': ultimo_encuentro,
        'proximos_encuentros': proximos_encuentros,
    }
    return render(request, 'prayer_meetings.html', context)


def downloads(request):
    """ 
    Documentos importantes que la iglesia permitr consultar a los usuarios
    por medio de descargas 
    """
    documentos = Documento.objects.order_by('-fecha_subida')
    return render(request, 'downloads.html', {'documentos': documentos})


def blogs(request):
    """ 
    Pantalla donde el usuario puede encontrar los diferentes blogs cargados
    en el sistema
    """
    blogs = Blog.objects.order_by('-fecha_publicacion')     # pylint: disable=redefined-outer-name
    return render(request, 'blogs.html', {'blogs': blogs})


def blog_detail(request, blog_id):
    """ 
    Detalle de cada uno de los blogs de la Iglesia con el objetivo de 
    poder informar al usuario 
    """
    blog = Blog.objects.get(id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})
