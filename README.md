一个基于`Django`开发的`SNMP`轮询Demo，可以对设备（代码内置了H3C OID部分规则）进行`SNMP`轮询，`icmp`连通性检测，并将结果写入数据库，前端页面读取数据库数据进行直观的展示。效果图可点击本页面导航栏的`Gallery`相册查看。

## 缘由

当初仅为了在项目实施中显示设备的上线情况和快速查找到需要变更配置的设备；后来越搞越多，像首页，设备导出，修改页，查看配置，计划任务，清空数据等功能并不是我当初有计划要制作的；最后及时刹车，许多脑中风暴的功能没有继续写，也没有继续添加功能的计划。

## 代码组成及工作流

**框架**

`Bootstrap-3.3.7`+`Django4.0.7`+`MySql-5.7.39`（或`sqlite`）

**工作流**

1. 设备初始参数写入数据库
2. 设备的轮询，并对结果进行写入数据库
3. 前端页面对数据的展示

## 页面及功能

1. 首页
   1. 设备类型统计显示
   2. 设备在线/离线、CPU使用率、内存使用率概览饼状图显示
   3. 设备CPU使用率、内存使用率 TOP 10 显示
   4. 关于
2. 设备管理
   1. 设备数据显示
   2. 设备添加
      1. snmp测试
      2. 继续添加
      3. 添加并返回
   3. 设备导出
   4. 设备详情
      1. 刷新
      2. 执行查看配置
   5. 设备参数修改、同步、删除
3. 计划任务
   1. 定时任务
   2. 手动任务
4. 更多操作
   1. 批量导入
   2. 清空数据

## 如何使用

**clone 仓库代码至本地或使用浏览器下载压缩包**

```
git clone https://github.com/kiraster/ndgv_demo.git
```

或 Code -->> Download ZIP


### 本地处理

使用任意支持Python 的 IDE工具，将代码目录添加


### 安装环境

**为了不影响你电脑的python环境，建议使用虚拟环境运行本代码**（以下用**Visual Studio Code** 软件举例）

1. IDE工具控制台切换到代码根目录

2. 创建虚拟环境

   ```
   python -m venv venv
   ```

3. 激活虚拟环境

   ```
   .\venv\Scripts\Activate.ps1
   ```

   可能遇到不能执行脚本的错误，可以以管理员身份打开`powershell`，执行` set-executionpolicy remotesigned`，选择`y`

#### 安装python 库

```
pip install -r requirements.txt
```

### 初始化数据库

1. 修改`ndgv1/settings.py `文件(78行开始)（以下是使用`sqlite`数据的配置，如需使用`MySQL`，把`sqlite`部分注释，再把`MySQL`注释部分取消即可）

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'ndgv1.3',  # 数据库名称
    #     'USER': 'root',
    #     'PASSWORD': 'xxxxxxxx',
    #     'HOST': '127.0.0.1',
    #     'PORT': 3306,
    #     'CHARSET': 'utf8'
    }
}
```

2. 删除`device_app/migrations` 和 `scheduler_app/migrations` 除`_init_.py `外的所有文件

3. 删除 `db.sqlite3` 文件

4. 执行数据库迁移命令

   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

### 修改`清空数据`功能代码

修改`device_app/views`文件(683行开始)，以下是使用`sqlite`数据的配置，如需使用`MySQL`，把`sqlite`部分注释，再把`MySQL`注释部分取消即可

```
只直接使用原生 sql 语句 更快
from django.db import connection
# sqlite 数据库
sqlite_db = connection.cursor()
# MySQL 数据库
# mysql_db = connection.cursor()
# 执行 命令 重置 自增ID
sqlite_db.execute('DELETE FROM sqlite_sequence')
sqlite_db.execute('DELETE FROM device_app_device')
sqlite_db.execute('DELETE FROM device_app_devicedetail')
sqlite_db.execute('DELETE FROM device_app_devicestate')
sqlite_db.execute('DELETE FROM device_app_devicelocation')
sqlite_db.execute('DELETE FROM scheduler_app_schedulerdetail')
sqlite_db.execute('DELETE FROM django_apscheduler_djangojob')
sqlite_db.execute('DELETE FROM django_apscheduler_djangojobexecution')
sqlite_db.execute('DELETE FROM sqlite_sequence')
# 取消外键约束
# mysql_db.execute('SET FOREIGN_KEY_CHECKS=0')
# mysql_db.execute('truncate table device_app_device')
# mysql_db.execute('truncate table device_app_devicedetail')
# mysql_db.execute('truncate table device_app_devicestate')
# mysql_db.execute('truncate table device_app_devicelocation')
# mysql_db.execute('truncate table scheduler_app_schedulerdetail')
# mysql_db.execute('truncate table django_apscheduler_djangojob')
# mysql_db.execute('truncate table django_apscheduler_djangojobexecution')
# 设置外键约束
# mysql_db.execute('SET FORE

```

## 运行代码

```
python .\manage.py runserver
```

## 代码弊端

1. 代码写死华三设备的oid
2. 代码中写死设备命名规则
3. 定时任务写死轮询时间
4. 前端页面展示以1080P分辨率屏幕编写
5. 首页展示，类别显示的规则写死华三设备型号
6. ……

## 可能的问题或错误

1. `PermissionError: [WinError 10013] `以一种访问权限不允许的方式做了一个访问套接字的尝试。
   1. 使用管理员权限运行IDE编辑器
   2. 检查是否端口占用
2. 设备管理页面显示的数据不正确
   1. 由于是内置华三部分设备的`OID`，有些设备的`OID`值没有添加到代码
   2. 有些数据根据设备命名规则解析出来的，如果设备名称不符合命名规则会显示不正确
3. 设备同步后显示同步成功，但是没有数据
   1. 可能是snmp团体字不正确，或IP地址不可达
   2. 或者本机防火墙限制
4. 批量导入失败
   1. 上传文件中格式不准确或数据有误
   2. 上传文件中数据与已有数据冲突，可使用清空数据再进行导入
   3. 由于没有加入Django事务，对于已导入正确数据并不会进行回退
5. 首页中类型统计不正确
   1. 统计规则是根据华三的设备型号中关键字定义的
   2. 其他厂商设备不通用
6. 页面显示不全或内容挤压
   1. 编写时候是以1080P分辨率屏幕显示为准
   2. 没有对其他分辨率屏幕做调整
