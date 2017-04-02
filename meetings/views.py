from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import ModelForm
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

from .models import Meeting
from tasks.models import Task
from rooms.models import Room


def index(request):
    if(request.user.is_authenticated == False):
        return redirect('/login')

    startdate = timezone.now()
    enddate = startdate + datetime.timedelta(days=5)

    m = Meeting.objects.filter(start__range=[startdate, enddate]).order_by('start')

    t = Task.objects.filter(meeting__in=m, complete='False')

    return render(request, 'index.html', {'user': request.user, 'meeting': m, 'task': t})


class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        exclude = ['creatingStaff']


def about(request):
    return render(request, 'about.html')


def create(request):

    if(request.user.is_authenticated == False):
        return redirect('/login')

    if request.method == 'POST':
        # print(request.POST)
        form = request.POST
        # u = User.objects.get(id=2)
        m = Meeting()
        m.name = form['Name']
        m.info = form['Info']
        m.creatingProfessor = form['CreatingProfessor']
        m.creatingStaff = request.user
        m.participants = form['Participants']
        m.start = form['Start']
        m.end = form['End']
        ven = Room.objects.get(id=form['Venue'])
        m.venue = ven
        m.save()

        if(len(form['tasks']) > 0):
            taskComma = form['tasks']
            taskComma = taskComma.replace(' ','')
            taskList = taskComma.split(",")

            for task in taskList:
                if(len(task)>0):
                    t = Task()
                    t.meeting = m
                    t.name = task
                    t.save()

        return render(request, 'meeting_success.html', {'msg': 'Created'})

    else:
        r = Room.objects.all()
        return render(request, 'create_meeting.html', {'user': request.user, 'room': r})

def view_list(request):

    if(request.user.is_authenticated == False):
        return redirect('/login')

    meetings = Meeting.objects.all()
    return render(request, 'view_meeting.html', {'user': request.user, 'meeting': meetings})


def individual_meeting(request):
    if(request.user.is_authenticated == False):
        return redirect('/login')

    if request.method == 'GET':
        meetid = request.GET['meetid']
        x = (Meeting.objects.get(id=(meetid)))
        return render(request, 'individual_meeting.html', {'user': request.user, 'meeting': x})

def delete(request):
    return HttpResponse('Delete')

def edit(request):
    if(request.user.is_authenticated == False):
        return redirect('/login')

    if request.method == 'POST':
        # print(request.POST)
        form = request.POST
        # u = User.objects.get(id=2)
        meetid = request.POST['meetid']
        m = Meeting.objects.get(id=meetid)
        oldtasks = Task.objects.filter(meeting=m)
        
        m.name = form['Name']
        m.info = form['Info']
        m.creatingProfessor = form['CreatingProfessor']
        m.creatingStaff = request.user
        m.participants = form['Participants']
        m.start = form['Start']
        m.end = form['End']
        ven = Room.objects.get(id=form['Venue'])
        m.venue = ven
        m.save()

        for i in oldtasks:
            # print('deleting...')
            i.delete()

        if(len(form['tasks']) > 0):
            taskComma = form['tasks']
            taskComma = taskComma.replace(' ','')
            taskList = taskComma.split(",")

            for task in taskList:
                if(len(task)>0):
                    t = Task()
                    t.meeting = m
                    t.name = task
                    t.save()

        return render(request, 'meeting_success.html', {'msg': 'Modified'})

    else:
        meetid = request.GET['meetid']
        x = Meeting.objects.get(id=meetid)
        r = Room.objects.all()
        t = Task.objects.filter(meeting=x)
        l = len(t)
        # print 'len: ', l
        tasks = ''
        for i,j in enumerate(t):
            # print i,j
            tasks += j.name 
            if(i != l-1):
                tasks += ', '

        # print(tasks)
        def formatdate(dt):
            start = ''
            start += str(dt.year) + '-'
            if(len(str(dt.month))==1):
                start += '0' + str(dt.month) + '-'
            else:
                start += str(dt.month) + '-'
            if(len(str(dt.day))==1):
                start += '0' + str(dt.day) 
            else:
                start += str(dt.day) 
            start += 'T'
            if(len(str(dt.hour))==1):
                start += '0' + str(dt.hour) + ':'
            else:
                start += str(dt.hour) + ':'
            if(len(str(dt.minute))==1):
                start += '0' + str(dt.minute) 
            else:
                start += str(dt.minute)

            return start

        s = formatdate(x.start + datetime.timedelta(hours=5,minutes=30))
        e = formatdate(x.end + datetime.timedelta(hours=5,minutes=30))
        # print(x.start,x.end)
        # print(s,e)

        return render(request, 'edit.html', {'user': request.user, 'meeting': x, 'room': r, 'tasks': tasks, 's': s, 'e': e})