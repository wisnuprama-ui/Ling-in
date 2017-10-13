from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
import requests
from .models import Friendship,Friend
from app_profile.models import UserProfile
from .forms import FriendForm
import requests
from ling_in import strings

response = {
    'TITLE':strings.TITLE,
    'YEAR':strings.YEAR,
}

# Create your views here.
def index(request, username=None):
    html = 'app_friend/add_friend.html'
    user=get_object_or_404(UserProfile,username=username)
    
    response['page_title'] = 'Friends'
    response['friends'] = get_query_friends(user)
    response['friend_form'] = FriendForm
    response['user'] = user
    return render(request, html, response)

def get_query_friends(user):
    friendship = Friendship.objects.filter(user=user)
    friends = []

    for f in friendship:
        friends.append(f.friend)

    return friends

def validate_url(url=str()):
    try:
        resp = requests.get(url)
        if(resp.status_code < 400):
            return True
    except requests.exceptions.MissingSchema:
        # the uxrl is not valid --> regex
        return False

    return False

def new_friend(request, username=None):

    user=get_object_or_404(UserProfile, username=username)

    form = FriendForm(request.POST or None)
    if(request.method == 'POST' and form.is_valid()):
        friend_name = request.POST['name']
        friend_url = request.POST['url']

        url_valid = validate_url(friend_url)

        if(url_valid):
            # if url is valid, then create the relation
            get_friend = Friend.objects.filter(url=friend_url)
            
            # check if friend is already in database
            if(len(get_friend) > 0):
                friend = get_friend[0]
            else:
                friend=Friend(name=friend_name, url=friend_url)
                friend.save()

            # check if the relation between user and friend is already created in the past
            # if true, then we won't make it.

            # get friendship that has relation with user and the friend
            # get_friendship = Friendship.objects.filter(user=user, friend=friend)

            Friendship(user=user, friend=friend).save()

        return HttpResponseRedirect('/%s/friends/' % (username))
    else:
        return HttpResponseRedirect('/%s/friends/' % (username))

def delete_friend(request, username=None, friend_id=None):
    """
    @TODO need to find the safe method to delete object
    :param request:
    :param username:
    :param status_id:
    :return:
    """
    model = Friend

    user = get_object_or_404(UserProfile, username=username)
    get_object_or_404(model, pk=friend_id).delete()
    return HttpResponseRedirect('/%s/friends/' % (user.username))