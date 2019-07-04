import os
import re
import shutil
import zipfile

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from project_models.models import YuanXingInfo
from website.settings import MEIDA_ROOT


# Create your views here.
def index(request):
    yx_names = YuanXingInfo.objects.all()
    return render(request, 'yuanxing/index.html', {'yx_names': yx_names})


@csrf_exempt
def del_yx(request):
    yx_name = request.POST.get('del_yx_name')
    yx_object = YuanXingInfo.objects.get(name=yx_name)
    yx_object.delete()

    return redirect('yuanxing:index')


@csrf_exempt
def add_yx(request):
    yx_name = request.POST.get('add_yx_name')
    if yx_name == '':
        return JsonResponse({'error': 'name must not be null'})
    if re.search('\W', yx_name):
        return JsonResponse({'error': 'name must not contains special characters'})
    if YuanXingInfo.objects.filter(name=yx_name):
        return JsonResponse({'error': 'this one is existed'})
    else:
        YuanXingInfo.objects.create(name=yx_name)
        return redirect('yuanxing:index')


@csrf_exempt
def edit_yx(request):
    upload = request.FILES.get('zip_info')

    if not upload:
        return JsonResponse({'error': 'you have not chose any zipfile'})

    yx_name = request.POST.get('yx_info')
    path = os.path.join(MEIDA_ROOT, 'yuanxing')
    dir_name = os.path.join(path, yx_name)
    upload_file = os.path.join(path, upload.name)

    if upload.name.replace('.zip', '') == yx_name:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)

        with open(upload_file, 'wb') as f:
            for content in upload.chunks():
                f.write(content)
        if request.META.get('HTTP_USER_AGENT').__contains__('Mac'):
            os.system('unzip %s -d %s' % (upload_file, path))
        else:
            f = zipfile.ZipFile(upload_file, 'r')
            for file in f.namelist():
                f.extract(file, path)

                absolute_file_src = os.path.join(path, file)
                # windows的zip文件中文传输进来之后是一个乱码的状态,zip默认是cp437编码,所以需要先编码成二进制,再解码成gbk
                absolute_file_des = os.path.join(path, file.encode('cp437').decode('gbk'))

                os.rename(absolute_file_src, absolute_file_des)
            f.close()
        os.remove(upload_file)

        return redirect('yuanxing:index')

    else:
        return JsonResponse({'error': 'filename mast be %s.zip' % yx_name})
