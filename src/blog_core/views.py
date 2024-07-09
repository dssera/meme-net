from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponse

from .forms import RegisterForm, LoginForm


def index(request):
    return HttpResponse('main blog page')

def account(request):
    return HttpResponse(f"hi, {request.user.username}");

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'blog_core/register.html', {'form': form})
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have signed up successfully')
            login(request, user)
            return redirect('account')
        else:
            return render(request, 'blog_core/register.html', {'form': form})

def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'blog_core/login.html', {'form': form})
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user:
                login(request, user)
                messages.success(request, 'You have signed in successfully')
                return redirect('account')

        messages.error(request, 'This user doesn\'t exist or data are invalid')
        return render(request, 'blog_core/login.html', {'form': form})
    
def sign_out(request):
    logout(request)
    messages.error(request, 'You have been logged out')
    return redirect('memes')
