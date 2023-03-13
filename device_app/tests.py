from django.test import TestCase

from device_app import models

# Create your tests here.
# 先查数据
# device_queryset = models.Device.objects.all()
res = models.Device.objects.filter(pk=1).first()
# print(device_queryset)
# res = device_obj.device_detail.all()
# print(res, type(res))
# print(res.device_detail.divce_sn)
# print
print(res.device_state.all())
print(res.device_state.all().values('ssh_state'))
