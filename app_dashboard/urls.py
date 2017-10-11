from django.conf.urls import url
from .views import index

urlpatterns = [
    url(r'^(?P<username>\w+)/stats/$', index, name='stats'),
]