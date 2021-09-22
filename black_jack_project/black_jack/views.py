from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
# Create your views here.

def register(request):
    if request.method == 'POST':
        User.objects.create_user(username = request.POST['username'],first_name=request.POST['first_name'], last_name=request.POST['last_name'],email=request.POST['email'], password=request.POST['password'])
        print(request)
        return redirect('/')
    return redirect('/')

def login_user(request):
    if request.method == 'POST':
        logged_user =authenticate(username=request.POST['username'],password=request.POST['password'])
        login(request,logged_user)
        return redirect('/')
    return redirect('/')

def logout_user(request):
    logout(request)
    return redirect('/')
  
def index(request):
	return render(request, 'index.html')
