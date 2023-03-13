# from ndgv1 import settings
# from datetime import datetime
# from cProfile import run
import time

from django.shortcuts import render
from django.views.generic.base import View

from django.http import JsonResponse

from scheduler_app import models as SA
from django_apscheduler import models as AP

from scheduler_app.scheduler_snmp import ApScheduler


# Create your views here.
# 计划任务视图
class IndexView(View):

    # 转换时间少八个时区，-_-
    def timestamp_to_date(self, time_stamp, format_string="%Y-%m-%d %H:%M:%S"):
        time_array = time.localtime(time_stamp)
        str_date = time.strftime(format_string, time_array)
        return str_date

    def get(self, request):
        # 查询 任务数据包 ， 返回前端页面查询对象
        manual_job_queryset = SA.SchedulerDetail.objects.all()

        # # 使用原生 sql 语句 查表
        # from django.db import connection
        # # MySQL 数据库
        # # mysql_db = connection.cursor()
        # with connection.cursor() as mysql_db:

        #     mysql_db.execute('select id,next_run_time from django_apscheduler_djangojob')
        #     res = mysql_db.fetchone()
        #     # print(res)

        # 使用 ORM 操作 查表
        # 查询DjangoJob表，默认内置只有一条定时任务
        job_queryset = AP.DjangoJob.objects.all()
        # 查 执行表，查最后一条记录 first last 不是根据id编号大小排的，这个数据表，可能与排序有关系
        last_job = AP.DjangoJobExecution.objects.first()
        # print(last_job.run_time)
        # t_time = self.timestamp_to_date(last_job.finished)
        # print(t_time, type(t_time))
        # print(last_job.run_time)

        return render(request, 'scheduler.html', locals())

    # 前端提交参数运行 任务
    def post(self, request):
        button_val = request.POST.get('button')
        # print(button_val)

        if button_val == 'add_job':

            back_dict = {'status_code': 1111}
            # 构造自建的任务数据表数据
            # exec_time = datetime.now()
            # from datetime import datetime
            # 写入数据库的时间，需要带时区，数据库时间存储使用UTC时间，不+8 ，直观显示比北京时间少8小时
            from django.utils import timezone
            exec_time = timezone.now()
            # print(exec_time)
            task_name = request.POST.get('task_name')

            # 判断数据库中是否有正在运行的SNMP轮询任务
            task_obj = SA.SchedulerDetail.objects.filter(task_type='SNMP同步',
                                                         task_state='执行中')
            if task_obj:
                back_dict = {'status_code': 4444}
                return JsonResponse(back_dict)
            # 写入任务数据表
            try:
                SA.SchedulerDetail.objects.create(task_name=task_name,
                                                  exec_time=exec_time)
            except Exception:
                back_dict = {'status_code': 5555}
                return JsonResponse(back_dict)

            # 触发调度任务

            job_obj = ApScheduler()
            job_obj.handle(task_name)

            # print(f'计划任务：{task_name},已添加')

            # back_dict['status_code'] = 2222
            back_dict = {'status_code': 1111}
            return JsonResponse(back_dict)

        elif button_val == 'job_interval':
            try:
                job_obj = ApScheduler()
                job_obj.handle2()

                back_dict = {'status_code': 1111}
                return JsonResponse(back_dict)
            except Exception:
                back_dict['status_code'] = 2222
                return JsonResponse(back_dict)

        else:
            back_dict['status_code'] = 4444
            return JsonResponse(back_dict)


# 调度管理视图
class DispatchManageView(View):

    # xxx
    def get(self, request):
        pass

    # 前端提交参数  执行 查看任务详情和删除任务
    def post(self, request):

        task_id = request.POST.get('task_id')
        button_val = request.POST.get('button')

        # 判断按钮值
        if button_val == 're_run':
            try:
                run_obj = SA.SchedulerDetail.objects.filter(pk=task_id, task_state='已完成').first()
                if run_obj:
                    task_name = run_obj.task_name

                    # 写入数据库的时间，需要带时区，数据库时间存储使用UTC时间，不+8 ，直观显示比北京时间少8小时
                    from django.utils import timezone
                    exec_time = timezone.now()
                    # 数据表 单行更新
                    run_obj.exec_time = exec_time
                    run_obj.task_state = '执行中'
                    run_obj.end_time = None
                    run_obj.save()

                    # 触发调度任务

                    job_obj = ApScheduler()
                    job_obj.handle(task_name)

                    back_dict = {'status_code': 1111}
                else:
                    back_dict = {'status_code': 3333}
            except Exception:
                back_dict = {'status_code': 2222}

        if button_val == 'task_delete':
            try:
                del_obj = SA.SchedulerDetail.objects.get(pk=task_id)
                # if del_obj.task_state == '执行中':
                #     back_dict = {'status_code': 3333}
                # else:
                #     del_obj.delete()
                #     back_dict = {'status_code': 1111}
                del_obj.delete()
                back_dict = {'status_code': 1111}
            except Exception:
                back_dict = {'status_code': 2222}

        return JsonResponse(back_dict)
