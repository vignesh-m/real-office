from django.test import TestCase
from .models import Meeting


class MeetingObjectTestCase(TestCase):

    def setUp(self):
        Meeting.objects.create(
            name='Test meeting',
            info='Meeting created as part of unit test',
            creatingProfessor='testprof'
        )

    def test_meeting_created(self):
        self.assertEqual(Meeting.objects.get(
            creatingProfessor='testprof').name, 'Test meeting')

    def test_particpants_list(self):
        mobj = Meeting.objects.get(creatingProfessor='testprof')
        participants = ['a1@gmail.com',
                        'cs14b055@smail.iitm.ac.in', 'a2@wrongmail.com']
        mobj.store_participants(participants)
        mobj.save()

        mobj = Meeting.objects.get(creatingProfessor='testprof')
        self.assertCountEqual(mobj.get_participants(), participants)
