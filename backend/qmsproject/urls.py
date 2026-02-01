from core.views import home
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("", home, name="home"),
    path("core/", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("anagrafiche/", include("anagrafiche.urls")),
    path("human_resources/", include("human_resources.urls")),
    path("acquistopelli/", include("acquistopelli.urls")),
    path("articoli/", include("articoli.urls")),
    path("manualeprocedure/", include("manualeprocedure.urls")),
    path("monitoraggi/", include("monitoraggi.urls")),
    path("manutenzioni/", include("manutenzioni.urls")),
    path("lwg/", include("lwg.urls")),
    path("autorizzazioni/", include("autorizzazioni.urls")),
    path("gestionerifiuti/", include("gestionerifiuti.urls")),
    path("nonconformity/", include("nonconformity.urls")),
    path("chem_man/", include("chem_man.urls")),
    path("antincendio/", include("antincendio.urls")),
    path("ricette/", include("ricette.urls")),
    path("air_emissions/", include("air_emissions.urls")),
    path("vendite/", include("vendite.urls")),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    # API
    path("api/accounts/", include("accounts.urls")),
    path("api/anagrafiche/", include("anagrafiche.api_urls")),
    path("api/articoli/", include("articoli.api_urls")),
    path("api/acquistopelli/", include("acquistopelli.api_urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
