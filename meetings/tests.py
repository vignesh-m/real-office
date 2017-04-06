from django.test import TestCase
from .models import Meeting
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.apps import apps

Room = apps.get_model('rooms', 'Room')


class MeetingObjectTestCase(TestCase):

    def setUp(self):
        room = Room.objects.create(name='Room1')
        Meeting.objects.create(
            name='Test meeting',
            info='Meeting created as part of unit test',
            creatingProfessor='testprof',
            creatingStaff=None,
            participants='[cs14b055]',
            venue=room,
        )
        Meeting.objects.create(
            name='Test meeting2',
            creatingProfessor='testprof2',
            venue=room,
        )

    def test_meeting_created(self):
        self.assertEqual(Meeting.objects.get(
            creatingProfessor='testprof').name, 'Test meeting')
        self.assertEqual(Meeting.objects.get(
            creatingProfessor='testprof2').name, 'Test meeting2')

    def test_particpants_list(self):
        mobj = Meeting.objects.get(creatingProfessor='testprof')
        participants = ['a1@gmail.com',
                        'cs14b055@smail.iitm.ac.in', 'a2@wrongmail.com']
        mobj.store_participants(participants)
        mobj.save()

        mobj = Meeting.objects.get(creatingProfessor='testprof')
        self.assertCountEqual(mobj.get_participants(), participants)

    def test_invalid_time(self):
        mobj = Meeting.objects.get(creatingProfessor='testprof')
        mobj.start = timezone.now()
        mobj.end = timezone.now() - timezone.timedelta(seconds=10)
        self.assertLess(mobj.end, mobj.start)
        self.assertRaises(ValidationError, mobj.full_clean)
        mobj.end = mobj.start + timezone.timedelta(seconds=10)
        mobj.full_clean()  # should not throw

    def test_meeting_clash(self):
        m1 = Meeting.objects.get(creatingProfessor='testprof')
        m2 = Meeting.objects.get(creatingProfessor='testprof2')
        room = Room.objects.get(name='Room1')
        self.assertEqual(m1.venue, room)
        self.assertEqual(m2.venue, room)
        m1.start = timezone.now()
        m1.end = timezone.now() + timezone.timedelta(seconds=10)
        m2.start = m1.end + timezone.timedelta(seconds=10)
        m2.end = m2.start + timezone.timedelta(seconds=10)
        m1.full_clean()  # valid
        m2.start = m1.end - timezone.timedelta(seconds=10)
        m1.save()
        m2.save()
        self.assertRaises(ValidationError, m1.full_clean)
        self.assertRaises(ValidationError, m2.full_clean)
