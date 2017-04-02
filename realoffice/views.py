from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib import messages


def login_view(request):
    if request.method == 'GET':
        for m in messages.get_messages(request):
            print(m)
        return render(request, 'login.html')
    else:
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            message = 'Incorrect Credentials'
            return render(request, 'login.html', {'error': message})
        return HttpResponseRedirect('/')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')
