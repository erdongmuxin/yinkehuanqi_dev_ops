from django.db import models


# Create your models here.

# 用户相关的model
class UserInfo(models.Model):
    username = models.CharField(max_length=10, null=False)
    password = models.CharField(max_length=20, null=False)
    position = models.ForeignKey('PositionInfo', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'userinfo'
        verbose_name_plural = '用户信息'


class PositionInfo(models.Model):
    post_name = models.CharField(max_length=10, null=False)

    def __str__(self):
        return self.post_name

    class Meta:
        db_table = 'positioninfo'
        verbose_name_plural = '职位'


# 主机相关的model
class MachineGroupInfo(models.Model):
    machinegroup = models.CharField(max_length=20, null=False, unique=True)

    def __str__(self):
        return self.machinegroup

    class Meta:
        db_table = 'machinegroupinfo'
        verbose_name_plural = '主机组'


class HostInfo(models.Model):
    hostname = models.CharField(max_length=20, null=False, unique=True)
    host = models.CharField(max_length=15, null=False, unique=True)
    port = models.IntegerField(null=False, default=2376)
    group = models.ForeignKey('MachineGroupInfo', on_delete=models.PROTECT)

    def __str__(self):
        return self.hostname

    class Meta:
        db_table = 'hosts'
        verbose_name_plural = '主机'

# docker 操作相关的model
# class DockerLogOperation(models.Model):
#     operation_name = models.CharField(max_length=50, null=False, unique=True)
#     operation
