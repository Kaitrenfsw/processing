"""service_TM URL Configuration

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
from django.contrib import admin
from django.conf.urls import url, include
from topic import views



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^topic/$', views.topic_list, name='topic-API'),
    url(r'^topicUser/$', views.topicUser_list, name='topicUser-API'),
    url(r'^keyword/$', views.keyword_list, name='keyword-API'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
