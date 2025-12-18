from django.shortcuts import render, redirect, render
from django.contrib.auth import logout, get_user_model
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User

# Importacion reset password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from smtplib import SMTPException

User = get_user_model()

# Vista cierre de sesión
def exit(request):
    logout(request)
    return redirect('/accounts/login/?next=/')

# Vista send reset password
def reset_password(request):
    if request.user.is_authenticated:
        return redirect('dashboard:inicio')
    else:
        if request.method == 'POST':
            # Obtener el nombre de usuario
            email = request.POST.get('email')
            try:
                user = User.objects.get(email=email)
                correo_usuario = user.email
                # Generar el token para el usuario
                token = default_token_generator.make_token(user)
                # Codificar el ID del usuario en base64
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                # Construir la URL para restablecer la contraseña
                reset_url = request.build_absolute_uri(f'/authentication/change_reset_password/{uid}/{token}/')
                # Renderizar la plantilla con los datos
                html_message = render_to_string(
                    'registration/reset_password/reset_password_email.html', 
                    {'reset_url': reset_url, 'user_name': user.username,}
                )
                # Construir el mensaje de correo electrónico
                subject = 'Restablecer contraseña'
                # Enviar el correo electrónico de restablecimiento de contraseña
                send_mail(subject, '', 'danielcccv2003@gmail.com', [correo_usuario], html_message=html_message)
                messages.success(request, 'Se ha enviado un correo electrónico de restablecimiento de contraseña a su dirección de correo electrónico.')
            except User.DoesNotExist:
                messages.error(request, '<strong>Error:</strong>El correo no existe en el sistema.')
            except SMTPException as e:
                messages.error(request, f'Hubo un problema al enviar el correo electrónico. <br><strong>Error:</strong> {e}')
            except Exception as e:
                messages.error(request, f'No se pudo conectar al servidor de correo. Verifica tu conexión a internet e inténtalo de nuevo. <br><strong>Error:</strong> {e}.')
            return redirect('authentication:reset_password')    
        else:
            return render(request, 'registration/reset_password/reset_password.html')
        
# Vista reset change password
def change_reset_password(request, uidb64, token):
    User = get_user_model()
    try:
        # Decodificar el ID del usuario y verificar el token
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        # Si el usuario y el token son válidos, procesar el formulario de cambio de contraseña
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Tu contraseña ha sido cambiada correctamente. Por favor, inicia sesión con tu nueva contraseña.')
                #return redirect('dashboard:inicio') 
        else:
            form = SetPasswordForm(user)
        return render(request, 'registration/reset_password/change_reset_password.html', {'form': form})
    else:
        #messages.error(request, 'El enlace de restablecimiento de contraseña no es válido. Por favor, intenta de nuevo.')
        return redirect('dashboard:inicio') 
