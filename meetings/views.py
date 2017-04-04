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
def report(request):
	pass

# Vishwanath
def periodicReport(request):
	pass

# Vishwanath
def adHocReport(request):
	pass

# Vishwanath
def expenditureReport(request):
	pass

# Vishwanath
def saveToPdf(request):
	pass
