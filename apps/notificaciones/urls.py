from django.urls import path
from apps.notificaciones import views

app_name = 'notificaciones'

urlpatterns = [
    path('', views.notifications, name="notifications"),
    path('notifications_mark_as_read/', views.notifications_mark_as_read, name="notifications_mark_as_read"),
    path('notifications_delete_all/', views.notifications_delete_all, name="notifications_delete_all"),
    path('detalle_notificacion/<int:pk_id>/', views.detalle_notificacion, name="detalle_notificacion"),
]