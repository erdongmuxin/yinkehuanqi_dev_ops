from django.http import JsonResponse
from django.shortcuts import render

from project_models.models import UserInfo


# Create your views here.
def index(request):
    if 'username' in request.session:
        username = request.session['username']
    else:
        username = '未登录'

    return render(request, 'user_operations/index.html', {'username': username})


def login(request):
    return render(request, 'user_operations/login.html')


def login_check(request):
    post_username = request.POST.get('username')
    post_password = request.POST.get('password')
    try:
        user = UserInfo.objects.get(username=post_username)
    except Exception:
        return JsonResponse({'res': 0})
    password = user.password

    if password == post_password:
        request.session['islogin'] = True
        request.session['username'] = user.username
        request.session.set_expiry(3600 * 24)
        return JsonResponse({'res': 1})
    else:
        return JsonResponse({'res': 0})
