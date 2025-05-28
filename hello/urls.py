from django.urls import path
from hello.views import hello_world
from hello.views import index
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('hello/', hello_world,name='hello_world'),
    path('ind/', index,name='index'),
    path('', index,name='index'),
    path('login/', auth_views.LoginView.as_view(template_name= "magazyn/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name= "magazyn/logout.html"), name="logout"),


]
