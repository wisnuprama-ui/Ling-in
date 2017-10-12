from django.db import models
from app_profile.models import UserProfile

class Friend(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    
    def __str__(self):
        return "%s - %s" % (
            self.name,
            self.url
        )

class Friendship(models.Model):
    friend = models.ForeignKey(Friend, models.CASCADE)
    user = models.ForeignKey(UserProfile, models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return "%s - %s" % (
            self.user.username,
            self.friend.name
        )

