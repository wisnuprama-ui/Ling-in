from django.conf.urls import url
from .views import index, new_friend


urlpatterns = [
    url(r'^(?P<username>\w+)/friends/$', index, name='index'),
    url(r'^(?P<username>\w+)/friends/add-friend/$', new_friend, name='add-friend')
 ]
