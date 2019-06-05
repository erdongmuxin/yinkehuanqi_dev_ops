import docker
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

tls_config = docker.tls.TLSConfig(
    client_cert=(
        r'/home/sd/python/devops/app/media/zhongnan_frontend/cert-zhongnan_frontend.pem',
        r'/home/sd/python/devops/app/media/zhongnan_frontend/key-zhongnan_frontend.pem'),
    verify=False
)
print(1)
client = docker.DockerClient(base_url='tcp://:2376', tls=tls_config, version='auto')

container = client.containers.list()


for i in container:
    print(i.name)
