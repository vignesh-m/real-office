import json
import datetime

from django.shortcuts import render, redirect
from django.forms import ModelForm
from django.utils import timezone, dateparse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from .models import Meeting
from tasks.models import Task
from rooms.models import Room


def index(request):
    html = """
    <h1> Welcome to RealOffice </h1>
    <p> <a href='/meeting/create'> Create Meeting </a> </p>
    <p> <a href='/meeting/list'> List Meetings </a> </p>
    """
    return HttpResponse(html)


class MeetingForm(ModelForm):

    class Meta:
        model = Meeting
        exclude = ['creatingStaff']


def create(request):
    if request.method == 'POST':
        # print(request.POST)
        form = MeetingForm(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponse('Meeting Created!')
        else:
            return HttpResponse('Invalid Meeting')
    else:
        form = MeetingForm()
        return render(request, 'create_meeting.html', {'form': form})


def view_list(request):
    html = ['<p>%s</p>' % str(m) for m in Meeting.objects.all()]
    return HttpResponse(html)

# Vishwanath
@login_required
def report(request):
	pass

# Vishwanath
@login_required
def periodicReport(request):
	pass

# Vishwanath
@login_required
def adHocReport(request):
	pass

# Vishwanath
@login_required
def expenditureReport(request):
	pass

# Vishwanath
@login_required
def saveToPdf(request):
	pass
