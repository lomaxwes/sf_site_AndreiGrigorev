import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from NewsPaper.settings import SITE_URL
from .models import PostCategory, Category, Post


def send_notifications(preview, pk, title, subscribers):
    html_context = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{SITE_URL}/posts/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()


def send_weekly_notifications():

    categories = Category.objects.all()
    for category in categories:
        subscribers = category.subscribers.all()
        posts = Post.objects.filter(category=category, time_date__gte=datetime.now() - datetime.timedelta(days=7))
        if posts.exists():
            subject = f'Новые статьи в категории {category.get_category_name_display()}'
            html_context = render_to_string(
                'weekly_notifications_email.html',
                {
                    'category': category,
                    'posts': posts,
                }
            )
            msg = EmailMultiAlternatives(
                subject=subject,
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[s.email for s in subscribers],
            )
            msg.attach_alternative(html_context, 'text/html')
            msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)