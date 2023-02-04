from django.core.mail import send_mail
from django.conf import settings

def send_forgotpassword(email, token):
    message = f'Click here to change your password http://localhost:8000/admins/reset-password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipent_list = [email]
    send_mail("Password Reset", message, email_from, recipent_list)