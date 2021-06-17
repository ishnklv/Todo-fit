from django.contrib import admin
from .models import Label, Task, UserAccount, Comment

admin.site.register(Task)
admin.site.register(Label)
admin.site.register(UserAccount)
admin.site.register(Comment)