from django.db import models
from app_profile.models import UserProfile

# Create your models here.

class Friend(models.Model):

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return "%s %s %s - %s" % (
            self.first_name,
            self.middle_name,
            self.last_name,
            self.link
        )

class Friendship(models.Model):
    friend = models.ForeignKey(Friend)
    user = models.ForeignKey(UserProfile)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)