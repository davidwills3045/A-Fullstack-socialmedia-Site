from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())

def setting(request):
    template = loader.get_template("setting.html")
    return HttpResponse(template.render())

def signin(request):
    template = loader.get_template("signin.html")
    return HttpResponse(template.render())

def signup(request):
    template = loader.get_template("signup.html")
    return HttpResponse(template.render())

def profile(request):
    template = loader.get_template("profile.html")
    return HttpResponse(template.render())