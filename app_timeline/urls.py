from django.conf.urls import url
from .views import (
    index, add_status, delete_status)

urlpatterns = [
    url(r'^(?P<username>\w+)/timeline/$', index, name='timeline_page'),
    url(r'^(?P<username>\w+)/timeline/add_status/$', add_status, name='add_status'),
    url(r'^(?P<username>\w+)/timeline/delete/(?P<status_id>[0-9]+)/$', delete_status, name='delete_status'),
]
