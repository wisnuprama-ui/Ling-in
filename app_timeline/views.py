from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ling_in import strings
from .models import Status, Comment
from app_profile.models import UserProfile
from .forms import StatusPostForm, CommentForm

# Create your views here.

response = {
    'TITLE': strings.TITLE,
    'YEAR': strings.YEAR,
}

class StatusComment:
    """
    without dictionary
    Status is an object and comment must be an iterable object like list or tuple
    """
    def __init__(self, status, comment=list()):
        self.status = status
        self.comment = comment
    
    def __str__(self):
        return "%s: %s" % (self.status, len(self.comment))
    
    def __repr__(self):
        return "%s: %s" % (self.status, len(self.comment))

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
    response['user'] = user
    response['status_form'] = StatusPostForm
    response['page_title'] = 'Timeline'

    status_post = get_queryset(user)
    page = request.GET.get('page', 1)
    numbers_of_status = range(len(status_post))
    paginator = Paginator(status_post, 10)

    no_post = True
    if(len(status_post) < 11):
        no_post = False

    try:
        status_stream = paginator.page(page)
    except PageNotAnInteger:
        status_stream = paginator.page(1)
    except EmptyPage:
        status_stream = paginator.page(paginator.num_pages)


    response['no_post'] = no_post
    response['status_stream'] = status_stream
    return render(request, template_name, response)


def get_queryset(user):
    """

    :param user:
    :return:
    """
    model = Status
    status_by_user = model.objects.all().order_by('-created_at') #for now we grab all status

    if(len(status_by_user) > 50):
        status_by_user = status_by_user[:50]

    status_with_comment = []
    ## this is bad ##
    for st in status_by_user:
        comment_for_this_st = Comment.objects.filter(status=st).order_by('-created_at')

        if(len(comment_for_this_st) > 10):
            comment_for_this_st = comment_for_this_st[:10]

        status_with_comment.append(
            StatusComment(
                status=st, 
                comment=comment_for_this_st
            )
        )

    return status_with_comment


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
        # messages.success(request, "Success")

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
    return HttpResponseRedirect('/%s/timeline/' % (user.username))

def index_comment(request, username=None, status_id=None):
    
    user = get_object_or_404(UserProfile, username=username)
    status = get_object_or_404(Status, pk=status_id)

    response['page_title'] = 'Comment'
    response['user'] = user
    response['status'] = status
    response['comment_form'] = CommentForm
    template_name = 'app_timeline/index_timeline_comment.html'
    return render(request, template_name, response)

def comment_status(request, username=None, status_id=None):
    # get commentator and status that commented by commentator
    user_commentator = get_object_or_404(UserProfile, username=username)
    status_commented = get_object_or_404(Status, pk=status_id)

    model = Comment
    form = CommentForm(request.POST or None)

    if(request.method == 'POST' and form.is_valid()):
        content = request.POST['content']
        # create comment
        model(user=user_commentator, status=status_commented, content=content).save()
        # messages.success(request, "Success")

        return HttpResponseRedirect('/%s/timeline/' % (username))

    else:
        return HttpResponseRedirect('/%s/timeline/' % (username))
    

    