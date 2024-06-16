from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from tracker.models.User import User


@receiver(post_save, sender=User)
def send_user_creation_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to our platform!'
        message = f'Hello {instance.first_name} {instance.last_name},\n\nWelcome to our platform. We are excited to have you!'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.email])
