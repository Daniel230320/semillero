from django.urls import path
from apps.lotes import views

app_name = 'lotes'

urlpatterns = [
    path('', views.listado_lotes, name="listado_lotes"),
    path('editar_lotes/<int:pk_id>/', views.editar_lotes, name="editar_lotes"),
]