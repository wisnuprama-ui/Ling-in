from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    """
    Description:
    Model for user app
    """
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICE = {
        MALE: 'Male',
        FEMALE: 'Female'
    }

    # basic user profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128) # store password with hashed, not raw password

    # custom
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    photo = models.ImageField(upload_to='images/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=6)

    # about
    description = models.CharField(max_length=500)
    #@TODO add expertise


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('username', 'name')