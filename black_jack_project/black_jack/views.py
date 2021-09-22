from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from django.template import loader
from django.http import HttpResponse

# Create your views here.

def index(request):
    context = {
        'RegForm': RegisterForm(),
        'LogForm': LoginForm(),
    }
    template = loader.get_template('index_modified.html')
    return HttpResponse(template.render(context, request))

def register(request):
    if request.method == 'POST':
        User.objects.create_user(username = request.POST['username'],first_name=request.POST['first_name'], last_name=request.POST['last_name'],email=request.POST['email'], password=request.POST['password'])
        print(request)
        return redirect('/dashboard')
    return redirect('/')

def login_user(request):
    if request.method == 'POST':
        logged_user =authenticate(username=request.POST['username'],password=request.POST['password'])
        login(request,logged_user)
        return redirect('/dashboard')
    return redirect('/')

def logout_user(request):
    logout(request)
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return render(request,'base_site.html')
    return redirect('/')

def html(request):
    pass 
 
'''
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request)) '''
