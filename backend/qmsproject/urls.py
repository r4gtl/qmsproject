"""
URL configuration for qmsproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from core.views import home
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path('', home, name='home'),
    path('core/', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('anagrafiche/', include('anagrafiche.urls')),
    path('human_resources/', include('human_resources.urls')),
    path('acquistopelli/', include('acquistopelli.urls')),
    path('articoli/', include('articoli.urls')),
    path('manualeprocedure/', include('manualeprocedure.urls')),
    path('monitoraggi/', include('monitoraggi.urls')),
    path('manutenzioni/', include('manutenzioni.urls')),
    path('lwg/', include('lwg.urls')),
    path('autorizzazioni/', include('autorizzazioni.urls')),
    path('gestionerifiuti/', include('gestionerifiuti.urls')),
    path('nonconformity/', include('nonconformity.urls')),
    path('chem_man/', include('chem_man.urls')),
    path('antincendio/', include('antincendio.urls')),
    path('ricette/', include('ricette.urls')),
    path('air_emissions/', include('air_emissions.urls')),
    path('vendite/', include('vendite.urls')),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)