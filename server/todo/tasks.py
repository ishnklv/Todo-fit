from django.core.mail import send_mail
from server import settings
from todo.models import Task
from django.utils import timezone
from celery import shared_task
import datetime

# Hello dev branch

@shared_task
def send_email_task():
    posts = Task.objects.all()
    now = datetime.datetime.now().replace(microsecond=0)
    print(str(now) + " --- " + str(posts))
    for post in posts:
        if post.date == now:
            send_mail('Notifiaction Todoist', f'Салам Алейкум! {post.user.first_name}\n Время вашего задания '
                                              f'истекает.\n <<{post.title}>>', settings.EMAIL_HOST_USER,
                      [post.user])
