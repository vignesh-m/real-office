from django.test import TestCase
from django.apps import apps

Meeting = apps.get_model('meetings', 'Meeting')


class RoomClashTestCase(TestCase):

    # t1 =

    def setUp(self):
        room1 = Room.object.create(name='Room1')
        Meeting.object.create(name='Meeting1', venue=room1, start=)

    # def
