from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Friendship


# Create your views here.
def index(request, username=None):
	html = 'app_friend/add_friend.html'
	#TODO Implement, isilah dengan 6 kata yang mendeskripsikan anda
	return render(request, html, response)

def get_query_friends(username):
	

def new_friend(request):
    form = Message_Form(request.POST or None)
    if(request.method == 'POST' and form.is_valid()):
        response['name'] = request.POST['name'] if request.POST['name'] 
        response['url'] = request.POST['url'] if request.POST['url'] 
        message = Message(name=response['name'], url=response['url'])
        message.save()
        html ='/form-result.html'
        return render(request, html, response)
    else:        
        return HttpResponseRedirect('/add-friend/')




