from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import PostCategory
from .tasks import send_notifications




@receiver(m2m_changed, sender=PostCategory)  # стандартный сигнал, есть в документации
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':

        postcategory = instance.postCategory.all()
        subscribers: list[str] = []
        for category in postcategory:
            subscribers += category.subscribers.all()

        subscribers_email = [s.email for s in subscribers]

        send_notifications.delay(instance.preview(), instance.pk, instance.title, subscribers_email)
