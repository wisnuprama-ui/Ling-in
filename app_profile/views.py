from django.shortcuts import render, get_object_or_404
from .models import UserProfile

# Create your views here.

response = {}

def index(request, username=None):

	user = get_object_or_404(UserProfile, username=username)
	response['user'] = user
	template_name = 'app_profile/index_profile.html'
	return render(request, template_name, response)

def edit(request, username=None):

	user = get_object_or_404(UserProfile, username=username)
	response['user'] = user
	template_name = 'app_profile/profile_edit.html'
	return render(request, template_name, response)