from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from ling_in.strings import TITLE, YEAR
from .forms import LoginForm, SignUpForm
from app_profile.models import UserProfile

# Create your views here.
respones = {
    'TITLE':TITLE,
    'YEAR':YEAR,
}

def index(request):
    template_name = 'app_home/index_login.html'

    respones['page_title'] = 'Home / Login'
    respones['login_form'] = LoginForm
    respones['message'] = 'Username'

    return render(request, template_name, respones)


def signup_account(request):
    template_name = 'app_home/index_account.html'

    respones['page_title'] = 'Home / Sign up'
    respones['signup_form'] = SignUpForm
    respones['message'] = 'Create Account'

    return render(request, template_name, respones)


def login_account(request):
    model = UserProfile
    form = LoginForm(request.POST or None)

    if(request.method == 'POST' and form.is_valid()):
        username = request.POST['username'].strip()
        # because username is unique so we just use filter
        search = UserProfile.objects.filter(username=username)

        if(len(search) != 1):
            messages.error(request, 'Username does not exist')
            return HttpResponseRedirect('/home/')

        user = search[0]
        return HttpResponseRedirect('/%s/timeline/' % (user.username))

    else:
        return HttpResponseRedirect('/home/')


def create_account(request):
    model = UserProfile
    form = SignUpForm(request.POST or None, request.FILES)

    if (request.method == 'POST' and form.is_valid()):
        username = request.POST['username'].strip()
        # because username is unique so we just use filter
        search = UserProfile.objects.filter(username=username)

        if (len(search) > 0):
            messages.error(request, 'Username not available')
            return HttpResponseRedirect('/home/account/')

        respones = request.POST

        user = model(
            username=username,
            first_name=respones['first_name'].strip(),
            middle_name=respones['middle_name'].strip(),
            last_name=respones['last_name'].strip(),
            email=respones['email'].strip(),
            gender=respones['gender']
        )
        user.save()

        return HttpResponseRedirect('/%s/timeline/' % (user.username))

    else:
        return HttpResponseRedirect('/home/account/')