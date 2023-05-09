from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate

from .forms import RegisterForm
from django.contrib.auth import logout

def register(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {"form": form})

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # check if user is in database
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # user is in database
            return HttpResponseRedirect("/")
        else:
            # user is not in database
            return render(request, 'registration/login.html', {"message": "Invalid credentials."})


    return render(request, 'registration/login.html', {})

def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html', {})