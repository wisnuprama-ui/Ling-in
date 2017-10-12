from django.conf.urls import url
from .views import (
    index, add_status, delete_status, comment_status, index_comment)

urlpatterns = [
    url(r'^(?P<username>\w+)/timeline/$', index, name='timeline_page'),
    url(r'^(?P<username>\w+)/timeline/add_status/$', add_status, name='add_status'),
    url(r'^(?P<username>\w+)/timeline/delete/(?P<status_id>[0-9]+)/$', delete_status, name='delete_status'),
    url(r'^(?P<username>\w+)/timeline/comment/(?P<status_id>[0-9]+)/$', index_comment, name='comment'),
    url(r'^(?P<username>\w+)/timeline/comment/(?P<status_id>[0-9]+)/$', comment_status, name='comment_status'),
]
