from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages

def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())

def setting(request):
    template = loader.get_template("setting.html")
    return HttpResponse(template.render())

def signin(request):
    return render(request,"signin.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"This email is already taken")
                return redirect("signup")
            elif User.objects.filter(username=username).exists():
                messages.info(request,"This username is already taken")
                return redirect("signup")
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
        else:
            messages.info(request,"password does not match" )
            return redirect("signup")
    else:      
        return render(request,"signup.html")

def profile(request):
    template = loader.get_template("profile.html")
    return HttpResponse(template.render())