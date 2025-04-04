# core/views.py
""" 
Recarga de las diferentes estancias necesarias para el funcionamiento 
de la App 
"""

import logging
from smtplib import SMTPException
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
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
    logger = logging.getLogger(__name__)

    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')

        # Construir el contenido del correo
        contenido = f"Nombre: {nombre}\nCorreo: {email}\nMensaje:\n{mensaje}"

        try:
            # Enviar el correo
            send_mail(
                subject='Nuevo mensaje de contacto',  # Asunto del correo
                message=contenido,  # Contenido del correo
                from_email='ing.jamescom@gmail.com',  # Remitente
                recipient_list=['osc_que@hotmail.com'],  # Destinatario
                fail_silently=False,
            )
            messages.success(request, 'Tu mensaje ha sido enviado exitosamente.')
            return redirect('contacto')
        except SMTPException as e:
            messages.error(request, f'Error al enviar el mensaje: {str(e)}')
        except Exception as e:
            # Usar formato % en lugar de f-strings
            logger.error('Error inesperado: %s', str(e))
            messages.error(request, 'Ha ocurrido un error inesperado. Inténtalo más tarde.')

    return render(request, 'contact.html')  # Renderiza la plantilla HTML


def contact_test(request):
    """ 
    Lugar donde el usuario puede ver las diferentes formas de contacto 
    con la iglesia, asì mismo por medio de un formulario puede enviar 
    un mensaje directo al email oficial de la iglesia
    """
    if request.method == 'POST':
        nombre = request.POST['nombre']
        email = request.POST['email']
        mensaje = request.POST['mensaje']

        # Construir el mensaje
        mensaje_completo = f'Nombre: {nombre}\nCorreo Electrónico: {email}\nMensaje:\n{mensaje}'

        # Enviar el correo
        send_mail(
            subject='Nuevo Mensaje de Contacto',
            message=mensaje_completo,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['osc_que@hotmail.com'],
        )

        # Mostrar un mensaje de éxito
        messages.success(request, 'Tu mensaje ha sido enviado con éxito.')
        return redirect('contact_test')  # Redirigir a la misma página después de enviar el mensaje

    return render(request, 'contact_test.html')


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
            filename=documento.archivo.name)
        return response
    except FileNotFoundError:
        raise Http404("Archivo no encontrado")


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
