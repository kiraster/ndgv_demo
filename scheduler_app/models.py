from django.db import models


# Create your models here.
class SchedulerDetail(models.Model):
    task_name = models.CharField(max_length=128, null=True, unique=True)
    task_type = models.CharField(max_length=32, null=True, default='SNMP同步')
    scheduler_type = models.CharField(max_length=32, null=True, default='手动')
    task_state = models.CharField(max_length=32, null=True, default='执行中')
    create_time = models.DateTimeField(auto_now_add=True)
    exec_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
