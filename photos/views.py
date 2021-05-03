from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, "login.html")

def register(request):
    errors=Register.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashedpw = bcrypt.hashpw(request.POST
        ['password'].encode(), bcrypt.gensalt()).decode()
        print(request.POST['password'])
        print(hashedpw)
        user = Register.objects.create(first_name=request.POST['first'], last_name=request.POST['last'], email=request.POST['email'], password=hashedpw)
        request.session['user']=user.id
        return redirect('/showimage')

def login(request):
    if request.method == 'POST':
        errors = Register.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user=Register.objects.get(email=request.POST['loginemail'])
            request.session['user']=user.id
            return redirect('/showimage')
    else:
        redirect('/')

def showimage(request):
    return render(request, "photoupload.html")

def store(request):
    newPhoto=Photos.objects.create(caption=request.POST['caption'], imagefile=request.FILES['image'], current_user=Register.objects.get(id=request.session['user']))
    return redirect('/showimage')