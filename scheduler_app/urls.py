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
# from device_app.views import IndexView
from scheduler_app.views import IndexView, DispatchManageView

urlpatterns = [
    # favicon.ico
    re_path(r'^favicon.ico$', RedirectView.as_view(url=r'static/img/favicon.ico')),
    # 设备添加
    path('', IndexView.as_view(), name='scheduler_app_task'),
    path('task/', DispatchManageView.as_view(), name='dispatch_manage'),
]
