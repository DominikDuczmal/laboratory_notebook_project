from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def signup_user(request):
    """Function allows to sign up a new User.

    It allows processing and validating a User Input, and logs him in.
    """

    if request.method == 'GET':
        return render(request, 'notebook/signup_user.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('get_analyst_form')
            except IntegrityError:
                return render(request, 'notebook/signup_user.html', {
                    'form': UserCreationForm(),
                    'error': 'That username has already been taken. Please choose a new username'
                })
        else:
            return render(request, 'notebook/signup_user.html', {
                'form': UserCreationForm(),
                'error': 'Passwords did not match'
            })


def login_user(request):
    """Function allows to log in a previously created User."""

    if request.method == 'GET':
        return render(request, 'notebook/login_user.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'notebook/login_user.html', {
                'form': AuthenticationForm(),
                'error': 'Username and password did not match'
            })
        else:
            login(request, user)
            return redirect('get_analyst_form')


@login_required
def logout_user(request):
    """Function allows to log out an active User."""

    if request.method == 'POST':
        logout(request)
        return redirect('home')
