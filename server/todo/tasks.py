from django.core.mail import send_mail
from server import settings
from todo.models import Task
from django.utils import timezone
from celery import shared_task
from datetime import datetime, timedelta


# Hello dev branch

@shared_task
def send_email_task():
    posts = Task.objects.filter(completed=False).filter(is_notific=False)
    now = datetime.now().replace(microsecond=0)
    for post in posts:
        post_date = post.date - timedelta(minutes=post.remind)
        print(str(now) + " ---- " + str(post_date))
        if post_date == now:
            send_mail('Notifiaction Todoist',
                      f'Привет! {post.user.first_name}\n У вас осталось 15 минут, чтобы успеть выполнить задание'
                      f'\n <<{post.title}>>', settings.EMAIL_HOST_USER,
                      [post.user], fail_silently=False)
            post.is_notific = True
        print(str(post.is_notific))
