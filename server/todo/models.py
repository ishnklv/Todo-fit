from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email


class Task(models.Model):
    REMIND = (
        (5, '5 min'),
        (10, '10 min'),
        (15, '15 min'),
        (30, '30 min'),
    )
    PRIORITY = (
        ('high', 'High'),
        ('normal', 'Normal'),
        ('low', 'Low')
    )
    user = models.ForeignKey('UserAccount', related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    date = models.DateTimeField(blank=True, null=True)
    parent = models.ForeignKey('self', related_name="children", on_delete=models.CASCADE, null=True, blank=True)
    is_notific = models.BooleanField(default=False)
    remind = models.IntegerField(choices=REMIND, null=True, blank=True)
    priority = models.CharField(choices=PRIORITY, max_length=50, null=True, blank=True)
    ordering = models.BigIntegerField(default=0)
    def __str__(self):
        return self.title

    # class Meta:
    #     ordering = ('ordering')


class Tag(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, related_name='tags', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, related_name='task', on_delete=models.CASCADE)
    title = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user, self.task)