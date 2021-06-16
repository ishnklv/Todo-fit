from django.core.mail import send_mail
from server import settings
from todo.models import Task
from django.utils import timezone
from celery import shared_task
from datetime import datetime, timedelta
# Hello dev branch

@shared_task
def send_email_task():
    posts = Task.objects.all()
    now = datetime.now().replace(microsecond=0)
    for post in posts:
        task = post.date - timedelta(minutes=15)
        print(str(now) + " ---- " + str(post.date))
        if task == now:
            send_mail('Notifiaction Todoist', f'Салам Алейкум! {post.user.first_name}\n У вас осталось 15 минут, чтобы успеть выполнить задание'
                                              f'\n <<{post.title}>>', settings.EMAIL_HOST_USER,
                      [post.user], fail_silently=False)