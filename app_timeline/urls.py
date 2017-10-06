from django.conf.urls import url
from .views import (
    index, add_status)

urlpatterns = [
    url(r'^(?P<username>\w+)/status/$', index, name='status_page'),
    url(r'^(?P<username>\w+)/status/add_status/$', add_status, name='add_status'),

]