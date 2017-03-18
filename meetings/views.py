from django.shortcuts import render
from django.http import HttpResponse
from django.forms import ModelForm

from .models import Meeting


def index(request):
    return HttpResponse("Hi")


class MeetingForm(ModelForm):

    class Meta:
        model = Meeting
        exclude = ['creatingStaff']


def create(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        print(form)
        return HttpResponse('Meeting Created!')
    else:
        form = MeetingForm()
        return render(request, 'create_meeting.html', {'form': form})
