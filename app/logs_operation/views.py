import re

import docker
import urllib3
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from project_models.models import HostInfo, MachineGroupInfo
from website import settings

# 消除警告信息
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def index(request):
    return render(request, 'logs_operation/index.html')


def connect_to_machine(hostname):
    try:
        tls_config = docker.tls.TLSConfig(
            client_cert=(r'%s/%s/cert-%s.pem' % (settings.MEIDA_ROOT, hostname, hostname),
                         r'%s/%s/key-%s.pem' % (settings.MEIDA_ROOT, hostname, hostname)),
            verify=False
        )
        client = docker.DockerClient(base_url='tcp://%s:2376' % hostname, tls=tls_config, version='auto')
        return client
    except docker.errors.TLSParameterError:
        return JsonResponse({'data': 0})


def machine_group(request):
    groups = MachineGroupInfo.objects.all()

    groups_list = []
    for group in groups:
        groups_list.append((group.id, group.machinegroup))

    return JsonResponse({'data': groups_list})


def machine_host(request, groupid):
    hosts = HostInfo.objects.filter(group_id=groupid)
    hosts_list = []
    for host in hosts:
        hosts_list.append((host.id, host.hostname))

    return JsonResponse({'data': hosts_list})


def containers_list(request, hostid):
    host = HostInfo.objects.get(id=hostid)
    containers = []
    client = connect_to_machine(host.hostname)
    try:
        for container in client.containers.list():
            containers.append(container.name)
        return JsonResponse({'data': containers})

    except AttributeError:
        return client


@csrf_exempt
def show_logs(request):
    hostid = request.POST.get('hostid')
    container = request.POST.get('container')
    length = request.POST.get('length')
    keyword = request.POST.get('keyword')
    if hostid != '---请选择主机---':
        host = HostInfo.objects.get(id=hostid)
        client = connect_to_machine(host.hostname)
        try:
            container = client.containers.get(container)

            if length != '':
                logs = container.logs(tail=int(length))
            else:
                logs = container.logs(tail=100)
            logs = logs.replace(b'\n', b'<br>')
            logs = logs.replace(b'\tat', b'&emsp;&emsp;')
            logs = logs.decode()
            logs_list = logs.split('<br>')
            logs = ''
            for i in logs_list:
                if re.search(keyword, i, flags=re.IGNORECASE):
                    logs += '%s<br>' % i
            if not logs:
                logs = '没有查到数据<br>'
            if keyword:
                keyword = keyword.replace(' ', '\\s+')
                word = re.findall(keyword, logs, re.I)
                Sword = set(word)
                for i in Sword:
                    logs = re.sub(i, '<font color=\"red\">%s</font>' % i, logs)
            return JsonResponse({'data': logs})
        except AttributeError:
            return client
        except docker.errors.NotFound:
            return JsonResponse({'data': 2})
    else:
        return JsonResponse({'data': 1})
