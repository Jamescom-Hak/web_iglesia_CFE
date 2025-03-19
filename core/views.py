# core/views.py
from django.utils import timezone
from django.shortcuts import render
from .models import About, Equipo, Evento, Documento, Blog

def home(request):
    eventos_destacados = Evento.objects.order_by('-fecha')[:3]
    ultimo_blog = Blog.objects.order_by('-fecha_publicacion').first()
    evento_especifico = Evento.objects.get(id=1)  # Cambia el ID por el de tu evento
    mensaje_pastor = "Jesucristo es el camino, la verdad y la vida. ¡Únete a nosotros para glorificar Su nombre!"
    return render(request, 'home.html', {
        'eventos': eventos_destacados,
        'mensaje_pastor': mensaje_pastor,
        'ultimo_blog': ultimo_blog,
        'evento_especifico': evento_especifico,
    })

def about(request):
    about_info = About.objects.first()  # Tomamos el primer registro (solo habrá uno)
    equipo = Equipo.objects.all()
    context = {
        'about': about_info,
        'equipo': equipo
    }
    return render(request, 'about.html', context)

def events(request):
    eventos = Evento.objects.order_by('-fecha')
    return render(request, 'events.html', {'eventos': eventos})

def resources(request):
    recursos = [
        {'titulo': 'Sermón: La Gracia de Dios', 'tipo': 'Audio', 'url': '#'},
        {'titulo': 'Devocional Semanal', 'tipo': 'PDF', 'url': '#'},
    ]
    return render(request, 'resources.html', {'recursos': recursos})

def contact(request):
    context = {
        'ubicacion': 'Calle Ejemplo 123, Ciudad, País',
        'email': 'contacto@iglesia.com',
        'telefono': '+123 456 7890',
    }
    return render(request, 'contact.html', context)

def prayer_meetings(request):
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
    documentos = Documento.objects.order_by('-fecha_subida')
    return render(request, 'downloads.html', {'documentos': documentos})

def blogs(request):
    blogs = Blog.objects.order_by('-fecha_publicacion')
    return render(request, 'blogs.html', {'blogs': blogs})

def blog_detail(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    return render(request, 'blog_detail.html', {'blog': blog})
