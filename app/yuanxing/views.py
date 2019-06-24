from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from project_models.models import YuanXingInfo


# Create your views here.
def index(request):
    yx_names = YuanXingInfo.objects.all()
    print(yx_names.query)
    return render(request, 'yuanxing/index.html', {'yx_names': yx_names})


@csrf_exempt
def del_yx(request):
    yx_name = str(request.POST.get('del_yx_name')).lstrip('删除')
    yx_object = YuanXingInfo.objects.get(name=yx_name)
    yx_object.delete()

    return redirect('yuanxing:index')


@csrf_exempt
def add_yx(request):
    yx_name = request.POST.get('add_yx_name')
    if YuanXingInfo.objects.filter(name=yx_name):
        return JsonResponse({'res': 0})
    else:
        print(yx_name)
        YuanXingInfo.objects.create(name=yx_name)
        return redirect('yuanxing:index')
