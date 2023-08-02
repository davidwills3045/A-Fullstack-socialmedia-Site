from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from .models import Profile
from django.contrib.auth.decorators import login_required


@login_required(login_url="signin")
def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())

@login_required(login_url="signin")
def setting(request):
    template = loader.get_template("setting.html")
    return HttpResponse(template.render())

def signin(request):
    if request.method=='POST' :
        username = request.POST["signin-username"]
        password = request.POST["signin-password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request,"Invalid credentials")
            return redirect("signin")
    else:
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

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username,password=password)
                auth.login(request, user_login)

                #create a profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect("setting")
        else:
            messages.info(request,"password does not match" )
            return redirect("signup")
    else:      
        return render(request,"signup.html")

def profile(request):
    template = loader.get_template("profile.html")
    return HttpResponse(template.render())

@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("signin")