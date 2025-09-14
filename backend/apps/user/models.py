from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.text import slugify


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        email_username = self.email.split('@')[0]
        if not self.username:
            self.username = slugify(email_username)
        super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='image', blank=True, null=True)
    bio = models.TextField(blank=True)
    about = models.TextField(blank=True, null=True, max_length=500)
    author = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
    def save(self, *args, **kwargs):
        if not self.user.username:
            email_username = self.user.email.split('@')[0]
            self.user.username = slugify(email_username)
            self.user.save()
        super().save(*args, **kwargs)
