from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from .models import Profile,Post,likePost,followersCount
from django.contrib.auth.decorators import login_required
from itertools import chain
import random


@login_required(login_url="signin")
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    user_following_list = []
    feed = []

    user_following = followersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestion_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestion_list = [x for x in list(new_suggestion_list) if (x not in list(current_user))]
    random.shuffle(final_suggestion_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestion_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_list = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_list)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    template = loader.get_template("index.html")
    context = {
        "user_profile" : user_profile,
        "posts" : feed_list,
        "suggestions_username_profile_list":suggestions_username_profile_list[:4],
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

@login_required(login_url="signin")
def profile(request,pk):
    user_object = User.objects.get(username =pk)
    user_profile = Profile.objects.get(user=user_object)
    # getting the amount of post a specific user has
    user_posts = Post.objects.filter(user=pk )
    user_post_length = len(user_posts)
    
    follower = request.user.username
    user = pk

    if followersCount.objects.filter(follower=follower,user=user).first():
        button_text = "Unfollow"
    else:
        button_text = "Follow"

    user_follower = len(followersCount.objects.filter(user=pk))
    user_following = len(followersCount.objects.filter(follower=pk))

    template = loader.get_template("profile.html")
    context = {
        "user_object" : user_object,
        "user_profile" : user_profile,
        "user_posts" : user_posts,
        "user_post_length" : user_post_length,
        "button_text" : button_text,
        "user_follower" : user_follower,
        "user_following" : user_following,
    }
    return HttpResponse(template.render(context,request))

@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("signin")

@login_required(login_url="signin")
def follow(request):
    if request.method == "POST":
        follower = request.POST["follower"]
        user = request.POST["user"]

            #unfollow
        if followersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = followersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect("/profile/" + user)
        else:
            # for unfollow
            new_follower = followersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect("/profile/" + user)
    else:
        return redirect('/')
    
@login_required(login_url="signin")
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == "POST":
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)
        
        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list)) 
        
        context = {
            "user_profile":user_profile,
            "username_profile_list" : username_profile_list,
        }
    else:
        pass

    return render(request,"search.html",context)

    

#     if request.method == "POST":
#         username = request.POST['username']
#         username_object = User.objects.filter(username__icontains=username)

#         username_profile = []
#         username_profile_list = []

#         for users in username_object:
#             username_profile.append(users.id)

#         for ids in username_profile:
#             profile_lists = Profile.objects.filter(id_user=ids)
#             username_profile_list.append(profile_lists)


#         username_profile_list = list(chain(*username_profile_list)) 
#     context = {
        # "user_profile":user_profile,
#         "username_profile_list":username_profile_list,
#     }