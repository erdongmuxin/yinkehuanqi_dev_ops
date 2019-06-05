from django.urls import path

from . import views

app_name = 'user_operations'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logincheck/', views.login_check, name='logincheck')
]