import datetime
import time

import docker
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

tls_config = docker.tls.TLSConfig(
    client_cert=(
        r'/home/sd/python/devops/app/media/zhongnan_backend/cert-zhongnan_backend.pem',
        r'/home/sd/python/devops/app/media/zhongnan_backend/key-zhongnan_backend.pem'),
    verify=False
)
print(1)
client = docker.DockerClient(base_url='tcp://zhongnan_backend:2376', tls=tls_config, version='auto')

container = client.containers.get('tomcat')
date = datetime.datetime.now()

while True:
    print(date)
    time.sleep(1)
    logs = container.logs(timestamps=True, since=10)
    print(logs.decode())
