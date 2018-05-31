from django.contrib import admin
from .models import Topic, TopicUser, Keyword

admin.site.register(Topic)
admin.site.register(TopicUser)
admin.site.register(Keyword)


