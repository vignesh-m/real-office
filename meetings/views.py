from django.shortcuts import render
from django.http import HttpResponse
from django.forms import ModelForm
from django.utils import timezone
import datetime

from .models import Meeting
from tasks.models import Task


def index(request):
    html = """
    <h1> Welcome to RealOffice </h1>
    <p> <a href='/meeting/create'> Create Meeting </a> </p>
    <p> <a href='/meeting/list'> List Meetings </a> </p>
    """
    # return HttpResponse(html)
    startdate = timezone.now()
    enddate = startdate + datetime.timedelta(days=5)

    m = Meeting.objects.filter(start__range=[startdate, enddate])
    # print len(m)

    t = Task.objects.filter(meeting__in=m)

    return render(request, 'index.html', {'meeting': m, 'task': t})


class MeetingForm(ModelForm):

    class Meta:
        model = Meeting
        exclude = ['creatingStaff']


def about(request):
    return render(request, 'about.html')


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
    # html = ['<p>%s</p>' % str(m) for m in Meeting.objects.all()]
    # return HttpResponse(html)
    # x = []
    meetings = Meeting.objects.all()
    # for m in meetings:
    #     x.append((str(m),m.id))

    return render(request, 'view_meeting.html', {'meeting': meetings})


def individual_meeting(request):
    if request.method == 'POST':
        # print request.POST
        meetid = request.POST['meetid']
        # print meetid
        x = (Meeting.objects.get(id=meetid))
        return render(request, 'individual_meeting.html', {'meeting': x})
