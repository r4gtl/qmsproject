from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .api import CurrentUserView, LogoutView, RegisterView
from .views import profile, registrazione_view

urlpatterns = [
    path("registrazione/", registrazione_view, name="registrazione_view"),
    path("profile/", profile, name="profile"),

    # API
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", CurrentUserView.as_view(), name="current_user"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

