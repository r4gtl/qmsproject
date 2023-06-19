from django.urls import path
from lwg.views import (lwg_home, lwg_procedure,
                                    )

app_name="lwg"

urlpatterns = [
    
    # Home LWG
    path('', lwg_home, name='lwg_home'),
    
    #LWG Procedure    
    path('lwg_procedure/<int:fk_lwgsection>', lwg_procedure, name='lwg_procedure'),    

    
]