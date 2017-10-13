from django.shortcuts import render, get_object_or_404
from .models import UserProfile, ExpertIn
from ling_in import strings

# Create your views here.

response = {
	'TITLE': strings.TITLE,
	'YEAR': strings.YEAR
}

def index(request, username=None):

	user = get_object_or_404(UserProfile, username=username)
	response['page_title'] = "Profile"
	response['user'] = user
	query = ExpertIn.objects.filter(user=user)
	user_expertise = []
	for exp in query:
		user_expertise.append(exp.expertise)

	response['user_expertise'] = user_expertise

	template_name = 'app_profile/index_profile.html'
	return render(request, template_name, response)

def edit(request, username=None):

	user = get_object_or_404(UserProfile, username=username)
	response['page_title'] = "Edit Profile"
	response['user'] = user
	template_name = 'app_profile/profile_edit.html'
	return render(request, template_name, response)

def post_custom_profile(request):

	if request.method == "POST" and form.is_valid():
		response['user'] = request.POST['user']
		newUserProfile = UserProfile(UserProfile, username=username)
		newUserProfile.save()
		template_name = '/app_profile/profile_edit.html'
		return render(request, template_name, response)
