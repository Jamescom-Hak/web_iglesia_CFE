"""
URL configuration for iglesiaCFE_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Ruta para la página de inicio
    path('about/', views.about, name='about'),
    path('events/', views.events, name='events'),
    path('resources/', views.resources, name='resources'),
    path('contact/', views.contact, name='contact'),
    path('contact_test/', views.contact_test, name='contact_test'),
    path('prayer-meetings/', views.prayer_meetings, name='prayer_meetings'),
    path('downloads/', views.downloads, name='downloads'),
    path('blogs/', views.blogs, name='blogs'),
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),
]
