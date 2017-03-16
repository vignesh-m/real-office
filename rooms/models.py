from __future__ import unicode_literals

from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=200)
    hasProjector = models.BooleanField(default=True)
    hasAC = models.BooleanField(default=False)
    hasMic = models.BooleanField(default=True)
