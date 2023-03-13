"""ndgv1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, re_path
from django.views.generic.base import RedirectView
# from device_app.views import IndexView, DeviceView, DeviceListView, DeviceDetailView, DeviceAddView, DeviceModifyView, DeviceDeleteView, DeviceSyncView, DeviceUploadView, DownloadView, DeleteAnythingView, SyncAnythingView
from device_app.views import IndexView, DeviceView, DeviceListView, DeviceDetailView, DeviceAddView, DeviceModifyView, DeviceDeleteView, DeviceSyncView, DeviceUploadView, DownloadView, DeleteAnythingView, SyncAnythingView

urlpatterns = [
    # 首页
    path('', IndexView.as_view(), name='index'),
    # favicon.ico
    re_path(r'^favicon.ico$', RedirectView.as_view(url=r'static/img/favicon.ico')),
    # 设备展示
    path('data/', DeviceView.as_view(), name='device_app'),
    path('list/', DeviceListView.as_view(), name='device_app_list'),
    # 设备详情
    path('detail/<int:device_id>/', DeviceDetailView.as_view(), name='device_app_detail'),
    # 设备添加
    path('add/', DeviceAddView.as_view(), name='device_app_add'),
    # 设备更新
    path('modify/', DeviceModifyView.as_view(), name='device_app_modify'),
    # 设备删除
    path('delete/', DeviceDeleteView.as_view(), name='device_app_delete'),
    # path('delete/<int:device_id>/', DeviceDeleteView.as_view(), name='device_app_delete'),
    # 设备同步
    path('sync/', DeviceSyncView.as_view(), name='device_app_sync'),
    # 上传
    path('upload/', DeviceUploadView.as_view(), name='device_app_upload'),
    # 下载
    path('template_download/', DownloadView.as_view(), name='device_app_template_download'),
    # 清空数据
    path('del_anything/', DeleteAnythingView.as_view(), name='device_app_del_anything'),
    # 同步所有
    path('sync_anything/', SyncAnythingView.as_view(), name='device_app_sync_anything'),
]
