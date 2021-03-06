from django.db import models
from TMengine.models import LdaModel


class Topic(models.Model):
    topic_number = models.IntegerField(null=False)
    lda_model = models.ForeignKey(LdaModel, on_delete=models.CASCADE, related_name='topic_ldamodel')
    name = models.CharField(null=True, blank=True, max_length=100)


class Keyword(models.Model):
    name = models.CharField(null=False, max_length=100)
    weight = models.FloatField()
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='keyword_topic')


class TopicUser(models.Model):
    user_id = models.IntegerField(null=False)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='user_topic')

    class Meta:
        unique_together = ("user_id", "topic_id")


