from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def user_directory_img_path(instance, filename):
    return 'image/user/{0}/profile/{1}'.format(instance.username, filename)


class Expertise(models.Model):
    """
    Description:
    Model for expertise by User

    """
    expertise = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.expertise

    class Meta:
        ordering = ('expertise', 'created_at')

class UserProfile(models.Model):
    """
    Description:
    Model for user app

    """
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICE = (
        (MALE,'Male'),
        (FEMALE, 'Female')
    )

    # basic user profile
    '''
    For now we don't have to make it as 'real user' that requires to login/logout
    what we need now is just it's profile
    '''
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # custom
    username = models.CharField(max_length=128, blank=False, unique=True)
    first_name = models.CharField(max_length=100, blank=False)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False, unique=True)
    birth_date = models.DateField(blank=False, null=True)
    birth_place = models.CharField(max_length=50, blank=False)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=6)
    description = models.CharField(default='', max_length=500, blank=True)
    photo = models.ImageField(upload_to=user_directory_img_path, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username', 'first_name', 'middle_name', 'last_name',
                    'birth_date', 'gender', 'created_at', 'updated_at')

class ExpertIn(models.Model):
    """
    Description:
    Model for bridging user with many expertise

    """
    user = models.ForeignKey(UserProfile)
    expertise = models.ForeignKey(Expertise)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False)