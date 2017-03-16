from __future__ import unicode_literals

from django.db import models
from meetings.models import Meeting


class Task(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    complete = models.BooleanField(default=False)
