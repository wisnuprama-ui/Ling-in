from django.conf.urls import url
from .views import index, login_account, signup_account, create_account

urlpatterns = [
    url(r'^home/$', index, name='homepage'),
    url(r'^account/$', signup_account, name='account'),
    url(r'^account/login/$', login_account, name='account_login'),
    url(r'^account/signup/$', create_account, name='account_signup'),
]