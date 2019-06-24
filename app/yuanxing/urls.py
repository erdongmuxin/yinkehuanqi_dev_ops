from django.urls import path

from . import views

app_name = 'yuanxing'
urlpatterns = [
    path('', views.index, name='index'),
    path('del_yx/', views.del_yx, name='del_yx'),
    path('add_yx/', views.add_yx, name='add_yx'),

]