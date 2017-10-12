#!/bin/bash
echo "Run unit test"
source env/bin/activate
echo "from app_profile.models import UserProfile;from django.utils import timezone;UserProfile.objects.filter(username='Anonymous').delete(); username = 'Anonymous';UserProfile(username=username,first_name=username,middle_name=username,last_name=username,email=username + '@' + username + '.com',birth_date=timezone.now(),birth_place=username,gender=UserProfile.MALE).save()" | python manage.py shell
coverage run --include='app_*/*' manage.py test
coverage report -m

