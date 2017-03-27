from django.shortcuts import render
from django.http import HttpResponse
from django.forms import ModelForm

from .models import Meeting


def index(request):
    html = """
    <h1> Welcome to RealOffice </h1>
    <p> <a href='/meeting/create'> Create Meeting </a> </p>
    <p> <a href='/meeting/list'> List Meetings </a> </p>
    """
    # return HttpResponse(html)
    return render(request, 'index.html')


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
    if request.method == 'POST':
        meetid = request.POST.meetid
        print meetid
        x = str(Meeting.objects.get(id=meetid))
        return HttpResponse(x)
        
    else:
        x = []
        meetings = Meeting.objects.all();
        for m in meetings:
            x.append((str(m),m.id))

        return render(request, 'view_meeting.html', {'meeting': x})