"""kofeFast URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import django.conf.urls.static
from django.contrib import admin
from django.urls import path

from kofe import views
from django.contrib.auth import views as auth_views

from kofeFast import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='index'),
    path('personal_area/', views.personal_area_page, name='personal_area'),
    path('change_password/', views.change_password, name='change_password'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] + django.conf.urls.static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              django.conf.urls.static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
