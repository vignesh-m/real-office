from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib import messages


def login_view(request):
    if request.method == 'GET':
        next1 = request.GET.get('next')
        if(next1 == None):
            next1 = '/'
        error = request.GET.get('error')
        if(error == None):
            error = 'nil'
        for m in messages.get_messages(request):
            print(m)
        return render(request, 'login.html', {'next': next1, 'error': error})

    else:
        # print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        next1 = request.POST['next']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            message = 'Incorrect Credentials'
            url = '/login/?next='+next1+'&'+'error='+message
            return HttpResponseRedirect(url)

        return HttpResponseRedirect(next1)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/?next=/')
