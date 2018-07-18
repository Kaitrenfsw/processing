from django.db import models


class New(models.Model):
    creation_date = models.DateField(auto_now=True)
    published = models.DateField(null=True)
    title = models.CharField(max_length=1000)
    text = models.TextField(null=True)
    url = models.TextField(null=True)
    site_name = models.TextField(null=True)
    site = models.TextField(null=True)
    main_image = models.TextField(null=True)
    used_to_classify = models.BooleanField(default=False)

