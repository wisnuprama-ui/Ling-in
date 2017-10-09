# testing
from django.conf.urls import url
from .views import index

urlpatterns = [
    url(r'^(?P<username>\w+)/$', index, name='profile_page'),
]