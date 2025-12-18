from django.urls import path
from apps.authentication import views

app_name = 'authentication'

urlpatterns = [
    path('reset_password/', views.reset_password, name="reset_password"),
    path('change_reset_password/<uidb64>/<token>/', views.change_reset_password, name='change_reset_password'),
    path('logout/', views.exit, name='exit'),
]