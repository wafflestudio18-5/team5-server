"""waffle_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from trelloclone.views import ping
from social.views import GoogleLogin

from django.urls import path

urlpatterns = [
    path('', ping),
    path('admin/', admin.site.urls),
    path('api/v1/', include('list.urls')),
    path('api/v1/', include('board.urls')),
    path('api/v1/', include('card.urls')),
    path('api/v1/', include('activity.urls')),
    path('api/v1/', include('user.urls')),
    #path('accounts/', include('allauth.urls')),
    #path('api/v1/user/social', TemplateView.as_view(template_name="login/index.html"))
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/google/$', GoogleLogin.as_view(), name='google_login')
]

if settings.DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
