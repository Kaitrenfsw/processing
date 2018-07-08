from django.db import models


class New(models.Model):
    creation_date = models.DateField(auto_now=True)
    publication_date = models.DateField(null=True)
    title = models.CharField(max_length=1000)
    description = models.TextField(null=True)
    full_text = models.TextField(null=True)
    info_source = models.TextField(null=True)
    image_source = models.TextField(null=True)
    used_to_classify = models.BooleanField(default=False)

