from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from .models import Profile,Post,likePost
from django.contrib.auth.decorators import login_required


@login_required(login_url="signin")
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    


    posts = Post.objects.all()
    template = loader.get_template("index.html")
    context = {
        "user_profile" : user_profile,
        "posts" : posts,
    }
    return HttpResponse(template.render(context,request))

@login_required(login_url="signin")
def like_post(request):
    username = request.user.username
    post_id = request.GET.get("post_id")

    post = Post.objects.get(id=post_id)
    like_filter = likePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = likePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect("/")
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect("/")
         
@login_required(login_url="signin")
def setting(request):
    user_profile = Profile.objects.get(user=request.user)
    myprofile = User.objects.all().values()
    context = {
        "user": myprofile,
        "user_profile": user_profile,
    }

    if request.method == "POST":

        if request.FILES.get("image") == None:
            image = user_profile.profileimage
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimage = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get("image") != None:
            image = request.FILES.get("image")
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimage = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect("setting")
    return render(request,"setting.html",context)

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

@login_required(login_url="signin")
def upload(request):

    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect("/")
    else:
        return redirect("/")


def profile(request):
    template = loader.get_template("profile.html")
    return HttpResponse(template.render())

@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("signin")