from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    """

    :param request:
    :param username:
    :return:
    """
    model = Status
    template_name = 'app_timeline/index_timeline.html'
    user = get_object_or_404(UserProfile, username=username)

    # get context
    respones['user'] = user
    respones['status_form'] = StatusPostForm
    respones['page_title'] = 'Timeline'

    status_post = get_queryset(user)
    page = request.GET.get('page', 1)
    numbers_of_status = range(len(status_post))
    paginator = Paginator(status_post, 10)

    try:
        status_stream = paginator.page(page)
    except PageNotAnInteger:
        status_stream = paginator.page(1)
    except EmptyPage:
        status_stream = paginator.page(paginator.num_pages)

    respones['status_stream'] = status_stream
    return render(request, template_name, respones)

def get_queryset(user):
    """

    :param user:
    :return:
    """
    model = Status
    return model.objects.filter(user=user).order_by('-created_at')


def add_status(request, username=None):
    """
    create new status based on user request
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

        return HttpResponseRedirect('/%s/timeline/' % (username))

    else:
        return HttpResponseRedirect('/%s/timeline/' % (username))


def delete_status(request, username=None, status_id=None):
    """
    @TODO need to find the safe method to delete object
    :param request:
    :param username:
    :param status_id:
    :return:
    """
    model = Status

    user = get_object_or_404(UserProfile, username=username)
    get_object_or_404(model, pk=status_id).delete()
    return HttpResponseRedirect('/%s/status/' % (user.username))