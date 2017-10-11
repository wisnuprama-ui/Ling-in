"""ling_in URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
import app_timeline.urls as app_timeline
import app_profile.urls as app_profile
import app_home.urls as app_home
import app_dashboard.urls as app_dashboard
import app_friend.urls as app_friend

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(app_home, namespace='app_home')),
    url(r'^', include(app_timeline, namespace='app_timeline')),
    url(r'^stats/', include(app_dashboard, namespace='app_dashboard')),
    url(r'^', include(app_friend, namespace='app_friend')),
    url(r'^', include(app_profile, namespace='app_profile')),
    # url(r'^', include(app_profile, namespace='app_profile')),
    # url(r'^', RedirectView.as_view(permanent='True', url='/home/'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)