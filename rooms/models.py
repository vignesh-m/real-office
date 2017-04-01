from __future__ import unicode_literals

from django.db import models
from meetings.models import Meeting


class Room(models.Model):
    name = models.CharField(max_length=200)
    hasProjector = models.BooleanField(default=True)
    hasAC = models.BooleanField(default=False)
    hasMic = models.BooleanField(default=True)
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def is_free(self, start_time, end_time):
        # Returns True if this room is free to use between start_time and
        # end_time, False otherwise

        def is_clash(st1, et1, st2, et2):
            # Returns True iff [st1, et1] intersects with [st2, et2]
            return (st1 <= st2 and et1 > st2) or (st2 <= st1 and et2 > st1)

        # meetings = Meeting.objects.filter(venue=self)
        meetings = self.meeting_set.all()
        for m in meetings:
            if is_clash(start_time, end_time, m.start, m.end):
                return False
        return True
