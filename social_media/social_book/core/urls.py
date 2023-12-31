from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    path('setting/', views.setting, name='setting'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('upload/', views.upload, name='upload'),
    path('follow/', views.follow, name='follow'),
    # path('follow2/', views.follow2, name='follow2'),
    path('search/', views.search, name='search'),
    path('like-post/', views.like_post, name='like-post'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
]