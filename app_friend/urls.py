from django.conf.urls import url
from .views import index, add_friend


urlpatterns = [
    url(r'^(?P<username>\w+)/friends/$', index, name='index'),
    url(r'^(?P<username>\w+)/friends/add-friend/$', add_friend, name='add-friend')
 ]
