# core/views.py
""" 
Recarga de las diferentes estancias necesarias para el funcionamiento 
de la App 
"""

from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
from core.models import About, Equipo, Evento, Documento, Blog


def home(request):
    """
    En Home mostramos los últimos 4 eventos destacados y el último blog publicado.
    """
    # Obtener los 4 eventos más recientes
    eventos_destacados = Evento.objects.order_by('-fecha')[:4]

    # Obtener el último blog publicado
    ultimo_blog = Blog.objects.order_by('-fecha_publicacion').first()

    # Renderizar la plantilla con los datos
    return render(request, 'home.html', {
        'eventos': eventos_destacados,
        'ultimo_blog': ultimo_blog,
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


def contact(request):
    """
      Pantalla para informar al usuario sobre como contactar con la Iglesia
      CFE Oriente y de como llegar a ella
    """

    return render(request, 'contact.html')


def resources(request):
    """ 
    Recursos documentales o audiovisuales para promover la enseñanza de 
    la palabra de Dios, de los diferentes ministerios o para cumplimiento 
    de actividades como el bautismo, etc.
    """
    recursos = [
        {
            'titulo': 'Alabanza: Recordando a Jesús',
            'interprete': 'Grupo de Alabanza, Ptr. Oscar Quevedo H.',
            'tipo': 'Video',
            'url': 'https://www.youtube.com/embed/-yq_W0WG_2k'  # URL modificada
        },
        {
            'titulo': 'Alabanza: En los montes, en los valles',
            'interprete': 'Grupo de Alabanza, Nataly Quevedo H.',
            'tipo': 'Video',
            'url': 'https://www.youtube.com/embed/Go4eyYfuha8'  # URL modificada
        }
    ]
    return render(request, 'resources.html', {'recursos': recursos})


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


def descargar_documento(request, pk):
    """  
    Descarga de documentos
    """
    documento = get_object_or_404(Documento, pk=pk)
    documento.descargas += 1
    documento.save()
    try:
        response = FileResponse(
            documento.archivo.open('rb'),
            as_attachment=True,
            filename=documento.archivo.name
        )
        return response
    except FileNotFoundError as exc:
        raise Http404("Archivo no encontrado") from exc

    # pylint: disable=unused-argument
    # Nota: `request` es un argumento necesario para manejar la solicitud HTTP.


def descargas_view(request):
    """  
    Descarga de vistas
    """
    documentos = Documento.objects.all()
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
