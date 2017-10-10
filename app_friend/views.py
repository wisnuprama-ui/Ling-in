from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Friendship,Friend
from app_profile.models import UserProfile
from .forms import FriendForm

response = {}

# Create your views here.
def index(request, username=None):
    html = 'app_friend/add_friend.html'
    user=get_object_or_404(UserProfile,username=username)
    response['friends'] = get_query_friends(user)
    response['friend_form'] = FriendForm
    return render(request, html, response)

def get_query_friends(user):
    friendship = Friendship.objects.filter(user=user)
    friends = []

    for f in friendship:
        friends.append(f.friend)

    return friends

def new_friend(request, username=None):

    user=get_object_or_404(UserProfile, username=username)

    form = FriendForm(request.POST or None)
    if(request.method == 'POST' and form.is_valid()):
        friend_name = request.POST['name']
        friend_url = request.POST['url'] 
        # message = Message(name=response['name'], url=response['url'])
        # message.save()
        friend=Friend(name=friend_name, url=friend_url)
        friend.save()

        Friendship(user=user, friend=friend).save()

        return HttpResponseRedirect('/%s/friends/' % (username))
    else:        
        return HttpResponseRedirect('/%s/friends/' % (username))




