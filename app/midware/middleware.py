import re

from django.shortcuts import redirect
#
from django.utils.deprecation import MiddlewareMixin


class RequireLoginMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, *args, **kwargs):
        # print(request.path)
        if 'islogin' in request.session or re.match('/login', request.path) or re.match('/admin/', request.path):
            return
        else:
            return redirect('uo_op:login')
