from django.core.mail import send_mail

def enviar_correo_bienvenida(correo_destino, nombre_usuario):
    asunto = "Bienvenido al Sistema Académico"
    mensaje = f"Hola {nombre_usuario}, tu cuenta ha sido creada exitosamente."
    
    send_mail(
        asunto,
        mensaje,
        "no-reply@sistema-academico.com",
        [correo_destino],
        fail_silently=False
    )
