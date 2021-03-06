"""pysat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include

import pysat.views as views

import session.urls
import user.urls
import program.urls
import message.urls
import school.urls
import file.urls

urlpatterns = [
    path('', views.test),
    path('myip', views.test_ip),

    url(r'^session/', include(session.urls)),
    url(r'^user/', include(user.urls)),
    url(r'^program/', include(program.urls)),
    url(r'^message/', include(message.urls)),
    url(r'^school/', include(school.urls)),
    url(r'^file/', include(file.urls))
]
