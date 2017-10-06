from django.contrib import admin
from .models import (UserProfile,
                     Expertise,
                     ExpertIn)

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Expertise)
admin.site.register(ExpertIn)
