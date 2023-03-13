from django.db import models


# Create your models here.
# 创建表关系， 先创建基表，然后再添加外键字段
class Device(models.Model):
    # 设备名称
    sysname = models.CharField(max_length=64, null=True, default='New Device')
    # 管理IP
    mgmt_ip = models.GenericIPAddressField(null=True, unique=True)

    # 设备和设备位置是一对多，设备是多的一方，外键放在设备这一方,
    # 默认与设备位置表的主键关联
    device_location = models.ForeignKey(to='DeviceLocation', default='1', on_delete=models.CASCADE)

    # 设备和设备状态是一对多，外键字段可以建在任一方，建议放在查询频率多的一方
    device_state = models.ForeignKey(to='DeviceState', default='2', on_delete=models.CASCADE)

    # 设备与设备详情表是一对一关系，外键字段建在任一都可以，建议放在查询频率多的一方
    device_detail = models.OneToOneField(to='DeviceDetail',
                                         null=True,
                                         on_delete=models.CASCADE)


class DeviceDetail(models.Model):
    mgmt_ip = models.GenericIPAddressField(null=True, unique=True)
    device_alias = models.CharField(max_length=128, null=True, default='-/-')
    net_area = models.CharField(max_length=32, null=True, default='-/-')
    device_type = models.CharField(max_length=32, null=True, default='-/-')
    device_model = models.CharField(max_length=32, null=True, default='-/-')
    device_version = models.CharField(max_length=64, null=True, default='-/-')
    device_sn = models.CharField(max_length=32, null=True, default='-/-')
    community_data = models.CharField(max_length=32, null=True, default='-/-')
    device_uptime = models.CharField(max_length=64, null=True, default='-/-')
    device_cpu = models.IntegerField(null=True)
    device_mem = models.IntegerField(null=True)
    device_power_state = models.IntegerField(null=True)
    device_fan_state = models.IntegerField(null=True)
    device_temperature = models.IntegerField(null=True)
    add_time = models.DateTimeField(auto_now_add=True)
    last_sync_time = models.DateTimeField(auto_now=True)


class DeviceState(models.Model):
    snmp_state = models.BooleanField()
    icmp_state = models.BooleanField()


class DeviceLocation(models.Model):
    device_location = models.CharField(max_length=32, null=True)
