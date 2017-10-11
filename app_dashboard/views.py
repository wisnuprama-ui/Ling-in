from django.shortcuts import render, get_object_or_404
from app_profile import models as app_profile_models
from app_timeline import models as app_status_models
from app_friend import models as app_friend_models

response ={}
# Create your views here.
def index(request, username=None):
    model_user = app_profile_models.UserProfile
    model_status = app_status_models.Status
    model_friend = app_friend_models.Friendship

    user = get_object_or_404(model_user,username= username)
    
    user_status = model_status.objects.filter(user=user)
    len_status = len(user_status)
    if(len_status > 0):
        latest_status = user_status[0]
    else:
        latest_status = False

    friendship = model_friend.objects.filter(user=user)
    jumlah_teman = friendship.count()

    response['user'] = user
    response['latest_status'] = latest_status
    response['len_status'] = len_status
    response['jumlah_teman'] = jumlah_teman

    template = 'app_dashboard/dashboard.html'
    return render(request, template, response)
