from django.conf.urls import url
from .views import index, login_account, signup_account, create_account

urlpatterns = [
    url(r'^home/$', index, name='homepage'),
    url(r'^home/login/$', login_account, name='login'),
    url(r'^home/account/$', signup_account, name='account'),
    url(r'^home/account/signup/$', create_account, name='signup'),
]