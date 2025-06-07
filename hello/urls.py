from django.urls import path
from django.urls import include
from hello.views import hello_world, item_list
from hello.views import index
from hello.views import inventory_list
from hello.views import gtin_inventory_list
from hello.views import product_details_view
from hello.views import upload_image
from hello.views import add_inventory_item
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('hello/', hello_world,name='hello_world'),
    path('ind/', index,name='index'),
    path('det/<int:pk>', product_details_view,name='details'),
    path('inventory/<str:pk>', gtin_inventory_list,name='gtin_inventory_list'),
    path('inventory/', inventory_list,name='inventory_list'),
    path('', item_list,name='item_list'),
    path('item/', item_list,name='item_list'),
    path('login/', auth_views.LoginView.as_view(template_name= "magazyn/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name= "magazyn/logout.html"), name="logout"),
    path('additem/', upload_image, name='upload_image'),
    path('addinv/', add_inventory_item, name='add_inventory_item'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)