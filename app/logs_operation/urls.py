from django.urls import path, re_path

from . import views

app_name = 'user_operations'
urlpatterns = [
    path('', views.index, name='index'),
    path('machine_group/', views.machine_group, name='machine_group'),
    re_path('machine_host/(\d*)', views.machine_host, name='machine_host'),
    re_path('container_list/(\d*)', views.containers_list, name='container_list'),
    path('show_logs/', views.show_logs, name='show_logs')
]
