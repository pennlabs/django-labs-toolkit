from django.db import models

from pennlabs.shortener.manager import UrlManager


class Url(models.Model):
    long_url = models.URLField()
    short_id = models.SlugField()

    def __str__(self):
        return f"{self.long_url} -- {self.short_id}"

    objects = UrlManager()
