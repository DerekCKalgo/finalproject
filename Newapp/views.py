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
    if 'user' in request.session:
        context={
            'all_photos': Photo.objects.all(),
            'current_user': Register.objects.get(id=request.session['user']),
            'all_comments': Comment.objects.all(),
            }
        return render(request, "photoupload.html", context)
    else:
        return redirect('/')

def store(request):
    newPhoto=Photo.objects.create(caption=request.POST['caption'], imagefile=request.FILES['image'], current_user=Register.objects.get(id=request.session['user']))
    return redirect('/showimage')

def like(request, photo_id):
    this_photo=Photo.objects.get(id=photo_id)
    this_photo.user_who_like.add(request.session['user'])
    this_photo.save()
    return redirect('/showimage')

def comment(request, photo_id):
    this_photo=Photo.objects.get(id=photo_id)
    this_comment=Comment.objects.create(comment=request.POST['comment'], user_who_comment=Register.objects.get(id=request.session['user']))
    this_comment.photos.add(this_photo)
    return redirect('/showimage')

def ranking(request):
    context={
        'rank_like': Photo.objects.all().order_by("Photo.objects.all().order_by('user_who_like').count()")
    }
    return render(request, "ranking.html", context)

def logout(request):
    del request.session['user'] 
    return redirect('/')