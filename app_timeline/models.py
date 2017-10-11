from django.db import models
from app_profile.models import UserProfile

# Create your models here.

class Status(models.Model):
    """
    Description:

    """
    user = models.ForeignKey(UserProfile)

    content = models.CharField(max_length=200, blank=False, null=False)
    likes = models.PositiveIntegerField(default=0, blank=True, editable=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return "%s\n%s" % (self.user.username, self.content)

    class Meta:
        ordering = ('created_at', 'updated_at')

#
# class Comment(models.Model):
#
#     user = models.ForeignKey