from django.db import models


class Topic(models.Model):
    topic_number = models.IntegerField(null=False)
    corpus_number = models.IntegerField(null=False)
    name = models.CharField(null=True, blank=True, max_length=100)


class Keyword(models.Model):
    name = models.CharField(null=False, max_length=100)
    weight = models.FloatField()
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='keyword_topic')


class TopicUser(models.Model):
    user_id = models.IntegerField(null=False, unique=True)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='user_topic')


