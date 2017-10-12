from app_profile.models import UserProfile
from django.utils import timezone

if("__main__" == __name__):
    username = 'anonymous'
    user_profile = UserProfile(
            username=username,
            first_name=username,
            middle_name=username,
            last_name=username,
            email=username + '@' + username + '.com',
            birth_date=timezone.now(),
            birth_place=username,
            gender=UserProfile.MALE,
            description=username + username + username
    )
    user_profile.save()