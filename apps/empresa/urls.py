from django.urls import path
from apps.empresa import views

app_name = 'empresa'

urlpatterns = [
    path('configuracion/', views.configuracion, name='configuracion'),
    path('ciudades_por_provincia/<int:provincia_id>/', views.ciudades_por_provincia, name='ciudades_por_provincia'),
]