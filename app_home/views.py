from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from ling_in.strings import TITLE, YEAR
from .forms import LoginForm, SignUpForm
from app_profile.models import UserProfile
from datetime import datetime

# Create your views here.
response = {
    'TITLE':TITLE,
    'YEAR':YEAR,
}

def index(request):
    template_name = 'app_home/index_login.html'

    response['page_title'] = 'Home'
    response['login_form'] = LoginForm
    response['message'] = 'Username'

    return render(request, template_name, response)


def signup_account(request):
    template_name = 'app_home/index_account.html'

    response['page_title'] = 'Home / Sign up'
    response['signup_form'] = SignUpForm
    response['message'] = 'Create Account'

    return render(request, template_name, response)


def login_account(request):
    model = UserProfile
    form = LoginForm(request.POST or None)

    if(request.method == 'POST' and form.is_valid()):
        username = request.POST['username'].strip()
        # because username is unique so we just use filter
        search = UserProfile.objects.filter(username=username)

        if(len(search) != 1):
            messages.error(request, 'Username does not exist')
            return HttpResponseRedirect('/')

        user = search[0]
        return HttpResponseRedirect('/%s/timeline/' % (user.username))

    else:
        return HttpResponseRedirect('/')


def create_account(request):
    model = UserProfile
    form = SignUpForm(request.POST or None, request.FILES)

    if (request.method == 'POST' and form.is_valid()):
        username = request.POST['username'].strip()
        # because username is unique so we just use filter
        search = UserProfile.objects.filter(username=username)

        if (len(search) > 0):
            messages.error(request, 'Username not available')
            return HttpResponseRedirect('/account/')

        response = request.POST

        user = model(
            username=username,
            first_name=response['first_name'].strip(),
            middle_name=response['middle_name'].strip(),
            last_name=response['last_name'].strip(),
            email=response['email'].strip(),
            gender=response['gender'],
            birth_date=response['date']
        )
        user.photo = form.cleaned_data['photo']
        user.save()

        return HttpResponseRedirect('/%s/timeline/' % (user.username))

    else:
        return HttpResponseRedirect('/account/')