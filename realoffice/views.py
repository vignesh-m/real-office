from django.shortcuts import render
from django.contrib.auth import authenticate, login


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        # user = authenticate(username, password)
        return render(request, 'about.html')
