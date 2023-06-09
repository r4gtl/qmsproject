from django.urls import path

from .views import (dashboard_acquisto_pelli,
                    LottoCreateView,
                    )

app_name="acquistopelli"



urlpatterns = [
    # Acquisto pelli dashboard
    path('', dashboard_acquisto_pelli, name="dashboard_acquisto_pelli"),
    path('acquisto_lotto', LottoCreateView.as_view(), name="acquisto_lotto"),
    

    
]