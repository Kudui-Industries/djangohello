from django.urls import path
from hello.views import hello_world, item_list
from hello.views import index
from hello.views import inventory_list
from hello.views import product_details_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('hello/', hello_world,name='hello_world'),
    path('ind/', index,name='index'),
    path('det/<int:pk>', product_details_view,name='details'),
    path('', inventory_list,name='inventory_list'),
    path('item', item_list,name='item_list'),
    path('login/', auth_views.LoginView.as_view(template_name= "magazyn/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name= "magazyn/logout.html"), name="logout"),


]
