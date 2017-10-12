from django.conf.urls import url
from .views import index, new_friend, delete_friend


urlpatterns = [
    url(r'^(?P<username>\w+)/friends/$', index, name='index'),
    url(r'^(?P<username>\w+)/friends/add_friend/$', new_friend, name='add_friend'),
    url(r'^(?P<username>\w+)/friends/delete_friend/(?P<friend_id>[0-9]+)/$', delete_friend, name='delete_friend')
 ]