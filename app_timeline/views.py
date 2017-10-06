from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.http import HttpResponseRedirect
from ling_in import strings
from .models import Status
from app_profile.models import UserProfile
from .forms import StatusPostForm

# Create your views here.

respones = {
    'TITLE': strings.TITLE,
    'YEAR': strings.YEAR,
}

def index(request, username=None):
        model = Status
        template_name = 'app_timeline/index_timeline.html'

        # get context
        respones['status_form'] = StatusPostForm
        respones['status_post'] = get_queryset(username)
        respones['pagetitle'] = username
        return render(request, template_name, respones)

def get_queryset(username):
    user = get_object_or_404(UserProfile, username=username)
    model = Status
    return model.objects.filter(user=user)[:10]

def add_status(request, username=None):
    """
    create new status based on user
    :param request:
    :param username:
    :return:
    """
    # get username
    model = Status
    user = get_object_or_404(UserProfile, username=username)
    form = StatusPostForm(request.POST or None)
    if(request.method == 'POST' and form.is_valid()):
        content = request.POST['content']
        # create status
        model(user=user, content=content).save()
        messages.success(request, "Success")

        return HttpResponseRedirect('timeline/%s/status/' % (username))

    else:
        return HttpResponseRedirect('timeline/%s/status/' % (username))
