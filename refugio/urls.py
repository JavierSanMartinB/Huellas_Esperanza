from django.urls import path, include

from django.conf.urls.static import static
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('personal/iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion_personal'),
    path('personal/cerrar-sesion/', views.cerrar_sesion_personal, name='cerrar_sesion_personal'),
    path('personal/animales/nuevo/', views.nuevo_animal, name='nuevo_animal'),
    path('animal/<int:animal_id>/', views.detalle_animal, name='detalle_animal'),
    path('registro/', views.registrar, name='registro'),
]