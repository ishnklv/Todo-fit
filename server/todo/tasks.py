from django.core.mail import send_mail
from server import settings
from todo.models import Task
from celery import shared_task
from datetime import datetime, timedelta
from fcm_django.models import FCMDevice

# Hello dev branch

@shared_task
def send_email_task():
    posts = Task.objects.filter(completed=False, is_notific=False)
    device = FCMDevice.objects.all().first()
    now = datetime.now().replace(microsecond=0, second=0)
    for post in posts:
        post_date = post.date - timedelta(minutes=post.remind)
        print(str(now) + ' --- ' + str(post_date))
        if post_date == now:
            # send_mail('Notifiaction Todoist',
            #           f'Привет! {post.user.first_name}\n У вас осталось {post.remind} минут, чтобы успеть выполнить задание'
            #           f'\n <<{post.title}>>', settings.EMAIL_HOST_USER,
            #           [post.user], fail_silently=False)
            device.send_message(title="Todo-fit", body=f'Hello {post.user.first_name}, Your task <<{post.title}>>')
            post.is_notific = True
            post.save()
