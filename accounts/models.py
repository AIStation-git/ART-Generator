from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import CustomUserManager
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    credit = models.IntegerField(default=6)
    contact_no = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)   
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_at =  models.DateField(auto_now=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
