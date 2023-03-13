# from datetime import datetime
from multiprocessing.pool import ThreadPool

from scheduler_app import snmp_polling
from device_app import models

from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from django_apscheduler.jobstores import DjangoJobStore


class AutoSNMP:

    # 获取管理IP，snmp团体字，返回生成器
    def scq(self):
        # queryset对象，管理IP，snmp团体字
        devicedetail_obj = models.DeviceDetail.objects.all()
        for row_obj in devicedetail_obj:
            polling_dict = {
                'mgmt_ip': row_obj.mgmt_ip,
                'community_data': row_obj.community_data,
            }
            yield polling_dict

    def do_polling(self):

        # 获取生成器
        polling_work = self.scq()
        # print(type(polling_work))
        # 异步执行获取写入的数据
        # ThreadPool 设定异步进程数为 x
        pool = ThreadPool(512)
        # sync_obj = Polling()
        for row_dict in polling_work:
            # device_data, detail_data = sync_obj.run(mgmt_ip, community_data)
            res = pool.apply_async(snmp_polling.run, args=(row_dict, ))
            # print(res.get())
            # 调用函数create_date 写入数据库
            self.create_date(row_dict['mgmt_ip'],
                             res.get()[0],
                             res.get()[1],
                             res.get()[2])

        pool.close()
        pool.join()

    def create_date(self, mgmt_ip, device_data, detail_data,
                    devicelocation_data):
        try:
            # 方式２，　update_or_create

            # 先查先写devicelocation 表，
            location_data = devicelocation_data['device_location']
            location_obj = models.DeviceLocation.objects.filter(
                device_location=location_data).first()
            if not location_obj:
                devicelocation_obj = models.DeviceLocation.objects.create(
                    device_location=location_data)
                device_location_id = devicelocation_obj
            else:
                device_location_id = location_obj.pk

            device_data['device_location_id'] = device_location_id

            # device_data写入device表, detail_data写入devicedetail表
            obj1, create1 = models.Device.objects.update_or_create(
                defaults=device_data, mgmt_ip=mgmt_ip)
            obj2, create2 = models.DeviceDetail.objects.update_or_create(
                defaults=detail_data, mgmt_ip=mgmt_ip)

            if create1 and create2:
                print('创建了一行数据！，不可能')
                print('永远不会打印这一行在控制台_ ^_^ _')
            else:
                # print('成功执行了写入数据库')
                pass
            return True
        except Exception:
            return False


class ApScheduler(AutoSNMP):

    # snmp轮询任务-手动一次性任务
    def snmp_polling_once(self, task_name):
        # start_time = datetime.now()
        self.do_polling()
        # end_time = datetime.now()
        # 写入数据库的时间，需要带时区，数据库时间存储使用UTC时间，不+8 ，直观显示比北京时间少8小时
        from django.utils import timezone
        end_time = timezone.now()
        update_dict = {'task_state': '已完成', 'end_time': end_time}

        # 填充任务数据表的任务结束时间，和任务状态
        from scheduler_app import models
        obj1, create1 = models.SchedulerDetail.objects.update_or_create(
            defaults=update_dict, task_name=task_name)
        # print(f'任务开始时间：{start_time}，任务结束时间：{end_time}')

    # snmp轮询任务-定时任务
    def snmp_job_interval(self):
        self.do_polling()

    from django_apscheduler import util

    # @util.close_old_connections
    # def delete_old_job_executions(self, max_age=604_800):
    #     from django_apscheduler.models import DjangoJobExecution
    #     DjangoJobExecution.objects.delete_old_job_executions(max_age)

    def handle(self, task_name):
        # from django.conf import settings
        # from apscheduler.schedulers.background import BackgroundScheduler
        # # from apscheduler.triggers.cron import CronTrigger
        # # from apscheduler.triggers.interval import IntervalTrigger
        # from apscheduler.triggers.date import DateTrigger
        # from django_apscheduler.jobstores import DjangoJobStore

        # scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler1 = BackgroundScheduler(timezone=settings.TIME_ZONE)
        scheduler1.add_jobstore(DjangoJobStore(), "default")

        scheduler1.add_job(
            self.snmp_polling_once,
            trigger=DateTrigger(),
            args=[
                task_name,
            ],
            id="snmp_job_once",
            max_instances=1,
            replace_existing=True,
        )

        # scheduler.add_job(
        #     self.delete_old_job_executions,
        #     trigger=CronTrigger(
        #         day_of_week="mon", hour="00", minute="00"
        #     ),  # Midnight on Monday, before start of the next work week.
        #     id="delete_old_job_executions",
        #     max_instances=3,
        #     replace_existing=True,
        # )

        try:
            scheduler1.start()
        except KeyboardInterrupt:
            scheduler1.shutdown()

    def handle2(self):
        # from django.conf import settings
        # from apscheduler.schedulers.background import BackgroundScheduler
        # # from apscheduler.triggers.cron import CronTrigger
        # from apscheduler.triggers.interval import IntervalTrigger
        # # from apscheduler.triggers.date import DateTrigger
        # from django_apscheduler.jobstores import DjangoJobStore

        # scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler2 = BackgroundScheduler(timezone=settings.TIME_ZONE)
        scheduler2.add_jobstore(DjangoJobStore(), "default")

        scheduler2.add_job(
            self.snmp_job_interval,
            trigger=IntervalTrigger(hours=1),  # Every 1 hour
            id="snmp_job_interval",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )

        try:
            scheduler2.start()
        except KeyboardInterrupt:
            scheduler2.shutdown()

        return scheduler2

    def get_job(self):
        job_obj = self.handle2()
        res = job_obj.get_job("snmp_job_interval")
        # job_obj.print_jobs()
        # print(res)
        return res
