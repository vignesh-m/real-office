import json
import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import ModelForm
from django.utils import timezone, dateparse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from .models import Meeting
from tasks.models import Task
from rooms.models import Room


@login_required
def index(request):
    startdate = timezone.now()
    enddate = startdate + datetime.timedelta(days=5)

    m = Meeting.objects.filter(
        start__range=[startdate, enddate]).order_by('start')

    t = Task.objects.filter(
        meeting__in=m, complete='False').order_by('meeting__start')
    cm = json.dumps([meeting.to_fc_event()
                     for meeting in Meeting.objects.all()])
    # print(cm)

    return render(request, 'index.html', {'user': request.user, 'meeting': m, 'task': t, 'cal_meetings': cm})


@login_required
def search_meeting(request):
    if(request.method == 'POST'):
        # print request.POST
        m = Meeting.objects.all()
        name = request.POST.get('Name')
        if(name != None):
            m = m.filter(name__contains=name)
        dt = request.POST.get('date')
        if(dt != None and len(dt) > 0):
            date = datetime.datetime.strptime(dt, "%Y-%m-%d").date()
            date1 = date + datetime.timedelta(days=1)
            m = m.filter(start__range=[date, date1]).order_by('start')
        # print m
        return render(request, 'view_meeting.html', {'user': request.user, 'meeting': m})

    return render(request, 'search.html')


@login_required
def task_done(request):
    # print request.POST
    for key in request.POST:
        if(key != 'csrfmiddlewaretoken'):
            t = Task.objects.get(id=key)
            value = request.POST[key]
            if(len(value) > 0):
                # print 'yes'
                t.complete = True
                t.cost = int(value)
                m = t.meeting
                m.expenditure += int(value)
                m.save()
                t.save()
                # print t.meeting.expenditure

    return redirect('/')


class MeetingForm(ModelForm):

    class Meta:
        model = Meeting
        exclude = ['creatingStaff']


@login_required
def about(request):
    return render(request, 'about.html')


@login_required
def success(request):
    return render(request, 'meeting_success.html')


@login_required
def create(request):
    # if not request.user.is_authenticated:
    #     messages.add_message(request, messages.ERROR,
    #                          'Login to Create Meetings')
    #     # return HttpResponseRedirect('/login', request=request)
    #     return redirect('login')
    def formatdate(dt):
        start = ''
        start += str(dt.year) + '-'
        if(len(str(dt.month)) == 1):
            start += '0' + str(dt.month) + '-'
        else:
            start += str(dt.month) + '-'
        if(len(str(dt.day)) == 1):
            start += '0' + str(dt.day)
        else:
            start += str(dt.day)
        start += 'T'
        if(len(str(dt.hour)) == 1):
            start += '0' + str(dt.hour) + ':'
        else:
            start += str(dt.hour) + ':'
        if(len(str(dt.minute)) == 1):
            start += '0' + str(dt.minute)
        else:
            start += str(dt.minute)

        return start

    tm = formatdate(timezone.now() + datetime.timedelta(hours=5, minutes=30))

    if(request.method == 'POST'):
        # print(request.POST)
        form = request.POST
        m = Meeting()
        m.name = form['Name']
        m.info = form['Info']
        m.creatingProfessor = form['CreatingProfessor']
        m.creatingStaff = request.user
        m.participants = form['Participants']
        m.start = timezone.make_aware(
            dateparse.parse_datetime(form['Start']), timezone.get_default_timezone())
        m.end = timezone.make_aware(
            dateparse.parse_datetime(form['End']), timezone.get_default_timezone())
        print(form['Start'], form['End'])
        ven = Room.objects.get(id=form['Venue'])
        m.venue = ven
        try:
            m.full_clean()
            m.save()
            if(len(form['tasks']) > 0):
                taskComma = form['tasks']
                # taskComma = taskComma.replace(' ','')
                taskList = taskComma.split(",")

                for task in taskList:
                    if(len(task) > 0):
                        t = Task()
                        t.meeting = m
                        t.name = task
                        t.save()

            return render(request, 'meeting_success.html', {'user': request.user, 'msg': 'Meeting Successfully Created'})
        except ValidationError as e:
            print(e)
            r = Room.objects.all()
            return render(request, 'meeting_success1.html', {'user': request.user, 'meeting': m, 'room': r, 'tasks': form['tasks'], 's': tm, 'e': tm})

    else:
        r = Room.objects.all()
        return render(request, 'create_meeting.html', {'user': request.user, 'room': r, 's': tm, 'e': tm})


@login_required
def view_list(request):
    meetings = Meeting.objects.all()
    return render(request, 'view_meeting.html', {'user': request.user, 'meeting': meetings})


@login_required
def report(request):
    if(request.method == 'POST'):
        # print request.POST
        m = Meeting.objects.all()
        name = request.POST.get('Name')
        if(name != None):
            m = m.filter(name__contains=name)
        dt = request.POST.get('start')
        dt1 = request.POST.get('end')
        if(dt != None and len(dt) > 0):
            date = datetime.datetime.strptime(dt, "%Y-%m-%d").date()
        if(dt1 != None and len(dt1) > 0):
            date1 = datetime.datetime.strptime(dt1, "%Y-%m-%d").date()

        m = m.filter(start__range=[date, date1]).order_by('start')
        total = 0
        for i in m:
            total += i.expenditure
        return render(request, 'report2.html', {'user': request.user,
                                                'meeting': m, 'start': date,
                                                'end': date1, 'total': total,
                                                'body': json.dumps(request.POST)})

    return render(request, 'report1.html', {'user': request.user})


@login_required
def report_pdf(request):
    print(request.GET)
    obj = json.loads(request.GET['report'])
    m = Meeting.objects.all()
    name = obj.get('Name')
    if(name != None):
        m = m.filter(name__contains=name)
    dt = obj.get('start')
    dt1 = obj.get('end')
    if(dt != None and len(dt) > 0):
        date = datetime.datetime.strptime(dt, "%Y-%m-%d").date()
    if(dt1 != None and len(dt1) > 0):
        date1 = datetime.datetime.strptime(dt1, "%Y-%m-%d").date()

    m = m.filter(start__range=[date, date1]).order_by('start')
    total = 0
    for i in m:
        total += i.expenditure
    return render(request, 'report2_min.html', {'user': request.user,
                                                'meeting': m, 'start': date,
                                                'end': date1, 'total': total})


@login_required
def individual_meeting(request):
    if (request.method == 'GET'):
        meetid = request.GET['meetid']
        x = (Meeting.objects.get(id=(meetid)))
        t = Task.objects.filter(meeting=x)
        l = len(t)
        # print 'len: ', l
        tasks = ''
        for i, j in enumerate(t):
            # print i,j
            tasks += j.name
            if(i != l - 1):
                tasks += ', '

        return render(request, 'individual_meeting.html', {'user': request.user, 'meeting': x, 'tasks': tasks})


@login_required
def delete(request):
    meetid = request.GET['meetid']
    x = Meeting.objects.get(id=meetid)
    x.delete()
    return render(request, 'meeting_success.html', {'user': request.user, 'msg': 'Meeting Successfully Deleted'})


@login_required
def edit(request):
    # if(request.user.is_authenticated == False):
    #     return redirect('/login')

    def formatdate(dt):
        start = ''
        start += str(dt.year) + '-'
        if(len(str(dt.month)) == 1):
            start += '0' + str(dt.month) + '-'
        else:
            start += str(dt.month) + '-'
        if(len(str(dt.day)) == 1):
            start += '0' + str(dt.day)
        else:
            start += str(dt.day)
        start += 'T'
        if(len(str(dt.hour)) == 1):
            start += '0' + str(dt.hour) + ':'
        else:
            start += str(dt.hour) + ':'
        if(len(str(dt.minute)) == 1):
            start += '0' + str(dt.minute)
        else:
            start += str(dt.minute)

        return start

    if (request.method == 'POST'):
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

        try:
            m.full_clean()

            if(len(form['tasks']) > 0):
                taskComma = form['tasks']
                # taskComma = taskComma.replace(' ','')
                taskList = taskComma.split(",")

                for i in oldtasks:
                    # print('deleting...')
                    if(i.name not in taskList):
                        m.expenditure -= i.cost
                        i.delete()
                    else:
                        taskList.remove(i.name)

                for task in taskList:
                    if(len(task) > 0):
                        t = Task()
                        t.meeting = m
                        t.name = task
                        t.save()

            else:
                for i in oldtasks:
                    m.expenditure -= i.cost
                    i.delete()

            m.save()
            return render(request, 'meeting_success.html', {'user': request.user, 'msg': 'Meeting Successfully Modified'})

        except ValidationError:
            r = Room.objects.all()
            s = formatdate(m.start)
            e = formatdate(m.end)
            return render(request, 'edit.html', {'msg': 'Room Unavailable at the Time. Try again.', 'user': request.user, 'meeting': m, 'room': r, 'tasks': form['tasks'], 's': s, 'e': e})

    else:
        meetid = request.GET['meetid']
        x = Meeting.objects.get(id=meetid)
        r = Room.objects.all()
        t = Task.objects.filter(meeting=x)
        l = len(t)
        # print 'len: ', l
        tasks = ''
        for i, j in enumerate(t):
            # print i,j
            tasks += j.name
            if(i != l - 1):
                tasks += ','

        s = formatdate(x.start + datetime.timedelta(hours=5, minutes=30))
        e = formatdate(x.end + datetime.timedelta(hours=5, minutes=30))

        # print(tasks)
        # print(x.start,x.end)
        # print(s,e)

        return render(request, 'edit.html', {'msg': 'none', 'user': request.user, 'meeting': x, 'room': r, 'tasks': tasks, 's': s, 'e': e})


@login_required
def add_room(request):
    if(request.method == 'POST'):
        # print request.POST
        r = Room()
        r.name = request.POST['Name']
        r.capacity = request.POST['capacity']
        temp = request.POST.get('hasAC')
        if(temp != None):
            r.hasAC = True
        else:
            r.hasAC = False
        temp = request.POST.get('hasMic')
        if(temp != None):
            r.hasMic = True
        else:
            r.hasMic = False
        temp = request.POST.get('hasProjector')
        if(temp != None):
            r.hasProjector = True
        else:
            r.hasProjector = False
        r.save()
        return redirect('/')

    return render(request, 'add_room.html', {'user': request.user})


@login_required
def available_rooms(request):
    # Get available rooms from time start to end
    # print(request.GET)
    all_rooms = Room.objects.all()
    try:
        start = timezone.make_aware(
            dateparse.parse_datetime(request.GET['start']), timezone.get_default_timezone())
        end = timezone.make_aware(
            dateparse.parse_datetime(request.GET['end']), timezone.get_default_timezone())
        need_proj = request.GET['has_proj'] == 'true'
        need_ac = request.GET['has_ac'] == 'true'
        need_mic = request.GET['has_mic'] == 'true'
        try:
            capacity = int(request.GET['capacity'])
        except ValueError:
            capacity = 0

        def is_ok(room):
            # return room.is_free(start, end)
            if not room.is_free(start, end):
                return False
            if need_ac and not room.hasAC:
                return False
            if need_proj and not room.hasProjector:
                return False
            if need_mic and not room.hasMic:
                return False
            if room.capacity < capacity:
                return False
            return True
        sugg = [{"id": r.id, "name": r.name}
                for r in all_rooms if is_ok(r)]
        rest = [{"id": r.id, "name": r.name}
                for r in all_rooms if not is_ok(r)]
    except Exception as e:
        print(e)
        sugg = [{"id": r.id, "name": r.name}
                for r in Room.objects.all()]
        rest = []
    return HttpResponse(json.dumps({
        "suggested": sugg,
        "rest": rest
    }))


@login_required
def get_notifications(request):
    startdate = timezone.now()
    enddate = startdate + datetime.timedelta(minutes=15)

    due_meetings = Meeting.objects.filter(
        start__range=[startdate, enddate]).order_by('start')

    notifs = [{
        "meeting": {"name": m.name, "id": m.id},
        "time": (m.start - startdate).seconds // 60
    } for m in due_meetings]
    return HttpResponse(json.dumps(notifs))
