from __future__ import unicode_literals
import json

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.core.exceptions import ValidationError
# from rooms.models import Room


class Meeting(models.Model):
    name = models.CharField(max_length=1000)
    info = models.TextField(blank=True, default='')
    creatingStaff = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    creatingProfessor = models.CharField(max_length=200, blank=True)
    participants = models.TextField(default='', blank=False, null=False)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)
    venue = models.ForeignKey(
        'rooms.Room', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return '%s on %s at %s' % (self.name, self.start, self.venue)

    # Vishwanath: To store the participants in text form
    def store_participants(self, participantList):
        delimiter = " "
        self.participants = delimiter.join(participantList)  # list -> string

    # Vishwanath: to get the participants in a list form
    def get_participants(self):
        delimiter = " "
        return self.participants.split(delimiter)   # string -> list

    def clean(self):
        # ensure room is not booked
        if not self.venue.is_free(self.start, self.end, self):
            raise ValidationError('room clash')
        # ensure start < end
        if self.start > self.end:
            raise ValidationError('meeting start must be before end')

    def to_fc_event(self):
        # convert to format required by caledar
        m = {
            'id': self.id,
            'title': self.name + ' at ' + str(self.venue),
            'start': self.start.isoformat(),
            'end': self.end.isoformat(),

        }
        return m
