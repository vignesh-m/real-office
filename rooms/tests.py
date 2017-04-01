from django.test import TestCase
from django.apps import apps
from django.utils import timezone
from datetime import datetime

from .models import Room

Meeting = apps.get_model('meetings', 'Meeting')

ist = timezone.get_default_timezone()
t3 = datetime(2017, 4, 1, 15, 0, tzinfo=ist)  # 3:00 pm
t330 = datetime(2017, 4, 1, 15, 30, tzinfo=ist)  # 3:30 pm
t315 = datetime(2017, 4, 1, 15, 15, tzinfo=ist)  # 3:15 pm
t350 = datetime(2017, 4, 1, 15, 50, tzinfo=ist)  # 3:50 pm
t4 = datetime(2017, 4, 1, 16, 00, tzinfo=ist)  # 4:00 pm
t430 = datetime(2017, 4, 1, 16, 30, tzinfo=ist)  # 4:30 pm
t415 = datetime(2017, 4, 1, 16, 15, tzinfo=ist)  # 4:15 pm


class RoomClashTestCase(TestCase):

    def setUp(self):
        self.room1 = Room.objects.create(name='Room1')
        self.room2 = Room.objects.create(name='Room2')
        Meeting.objects.create(name='Meeting1', venue=self.room1,
                               start=t3, end=t330)
        Meeting.objects.create(name='Meeting2', venue=self.room2,
                               start=t350, end=t4)

    def test_free(self):
        self.assertTrue(self.room1.is_free(t415, t430))
        self.assertFalse(self.room1.is_free(t315, t350))
        self.assertFalse(self.room2.is_free(t330, t430))

        self.assertTrue(self.room1.is_free(t330, t350))
        self.assertFalse(self.room1.is_free(t3, t315))
        self.assertFalse(self.room2.is_free(t330, t4))

    def test_room_available(self):
        self.assertCountEqual(Room.get_available(
            t3, t350), [self.room2])
        self.assertCountEqual(Room.get_available(
            t4, t430), [self.room1, self.room2])
        self.assertCountEqual(Room.get_available(
            t315, t415), [])
