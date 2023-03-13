import datetime
from pysnmp.entity.rfc3413.oneliner import cmdgen
import ping3


class Polling:

    def __init__(self):
        # icmp 结果存储字典
        self.icmp_state_dict = {}
        # pysnmp 结果存储字典
        self.pysnmp_dict = {}

        # 返回结果字典
        self.device_t_dict = {}
        self.deivcedetail_t_dict = {}
        self.deivcelocation_t_dict = {'device_location': 'Unknown'}

    # ping检测
    def icmp_polling(self, mgmg_ip):

        if ping3.ping(mgmg_ip):
            self.icmp_state_dict['icmp_state'] = True
            # print('通')
        else:
            # self.icmp_state_dict['icmp_state'] = False
            # print('不通')
            pass
        return self.icmp_state_dict

    # snmp轮询
    def do_pysnmp(self, mgmt_ip, community_data):

        try:

            cmdGen = cmdgen.CommandGenerator()

            # 定义字典 存入查询结果

            errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                cmdgen.CommunityData(community_data),
                cmdgen.UdpTransportTarget(
                    (mgmt_ip, 161)), '1.3.6.1.2.1.1.1.0', '1.3.6.1.2.1.1.3.0',
                '1.3.6.1.2.1.1.5.0', '1.3.6.1.2.1.47.1.1.1.1.10.1',
                '1.3.6.1.2.1.47.1.1.1.1.10.2', '1.3.6.1.2.1.47.1.1.1.1.11.1',
                '1.3.6.1.2.1.47.1.1.1.1.11.2', '1.3.6.1.2.1.47.1.1.1.1.10.4',
                '1.3.6.1.2.1.47.1.1.1.1.13.1', '1.3.6.1.2.1.47.1.1.1.1.13.2',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.18',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.4',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.66',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.212',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.97',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.25',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.14',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.175',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.18',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.4',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.66',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.212',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.97',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.25',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.14',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.175',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.468',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.158',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.66',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.212',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.97',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.314',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.18',
                '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.338',
                '1.3.6.1.4.1.25506.8.35.9.1.2.1.2.1',
                '1.3.6.1.4.1.25506.8.35.9.1.2.1.2.2',
                '1.3.6.1.4.1.25506.8.35.9.1.1.1.1.1')

            # Check for errors and print out results
            if errorIndication:
                print(mgmt_ip + '_' + errorIndication)
                # print(f'这个oid{str(varBinds[0])}没查到东西')
                return self.pysnmp_dict
            else:
                if errorStatus:
                    print(
                        '%s at %s' %
                        (errorStatus.prettyPrint(),
                         errorIndex and varBinds[int(errorIndex) - 1] or '?'))
                    return self.pysnmp_dict
                else:
                    # print(varBinds, type(varBinds))
                    for name, val in varBinds:

                        # print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
                        if str(name) == '1.3.6.1.2.1.1.1.0':
                            # print(f'设备系统描述：{val}')
                            # self.pysnmp_dict['sysdescr'] = str(val)
                            pass

                        elif str(name) == '1.3.6.1.2.1.1.3.0':
                            # print(f'设备启动时间：{val}')
                            # 获取到的是 timeticks value ，需要转换成人类能看懂的时间
                            device_uptime = datetime.timedelta(
                                seconds=int(val) / 100)
                            # 移除秒后的小数位
                            device_uptime = str(device_uptime).split('.')[0]
                            # print(sysuptime, type(sysuptime))
                            self.pysnmp_dict['device_uptime'] = device_uptime

                        elif str(name) == '1.3.6.1.2.1.1.5.0':
                            # print(f'设备名称：{val}')
                            self.pysnmp_dict['sysname'] = str(val)

                        elif str(name) in [
                                '1.3.6.1.2.1.47.1.1.1.1.10.1',
                                '1.3.6.1.2.1.47.1.1.1.1.10.2',
                                '1.3.6.1.2.1.47.1.1.1.1.10.4'
                        ]:
                            if str(val):
                                # print(f'设备系统软件版本：{val}')
                                self.pysnmp_dict['device_version'] = str(val)

                        elif str(name) in [
                                '1.3.6.1.2.1.47.1.1.1.1.11.1',
                                '1.3.6.1.2.1.47.1.1.1.1.11.2'
                        ]:
                            if str(val):
                                # print(f'设备序列号：{val}')
                                self.pysnmp_dict['device_sn'] = str(val)

                        elif str(name) in [
                                '1.3.6.1.2.1.47.1.1.1.1.13.1',
                                '1.3.6.1.2.1.47.1.1.1.1.13.2'
                        ]:
                            if str(val):
                                # print(f'设备型号：{val}')
                                self.pysnmp_dict['device_model'] = str(val)

                        elif str(name) in [
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.18',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.4',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.66',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.212',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.97',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.25',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.14',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.6.175'
                        ]:
                            if str(val) and str(val) not in '0':
                                # print(f'设备CPU利用率：{val}')
                                self.pysnmp_dict['device_cpu'] = str(val)

                        elif str(name) in [
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.18',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.4',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.66',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.212',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.97',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.25',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.14',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.8.175'
                        ]:
                            if str(val) and str(val) not in '0':
                                # print(f'设备内存利用率：{val}')
                                self.pysnmp_dict['device_mem'] = str(val)

                        elif str(name) in [
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.468',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.158',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.66',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.212',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.97',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.314',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.18',
                                '1.3.6.1.4.1.25506.2.6.1.1.1.1.12.338'
                        ]:
                            if str(val) and str(val) != '65535':
                                # print(f'设备温度：{val}')
                                self.pysnmp_dict['device_temperature'] = str(
                                    val)

                        elif str(name) in [
                                '1.3.6.1.4.1.25506.8.35.9.1.2.1.2.1',
                                '1.3.6.1.4.1.25506.8.35.9.1.2.1.2.2'
                        ]:
                            # print(f'设备电源状态：{val}')
                            if str(val) == '1':
                                self.pysnmp_dict['device_power_state'] = int(
                                    val)

                        elif str(name) == '1.3.6.1.4.1.25506.8.35.9.1.1.1.1.1':
                            if str(val):
                                # print(f'设备风扇状态：{val}')
                                self.pysnmp_dict['device_fan_state'] = int(val)
                            else:
                                self.pysnmp_dict['device_fan_state'] = 4

                        else:
                            print('有东西没查到哦')

                    # 返回字典给调用
                    return self.pysnmp_dict
        except Exception as e:
            # return False, e + 'The SNMP of this device is not working.'
            print(type(e))
            print(str(e))
            print(f'IP地址 {mgmt_ip} snmp查询出错!')
            return self.pysnmp_dict

    # 轮询结果处理
    def res_process(self):

        # 处理返回给device表的数据
        if self.icmp_state_dict and self.pysnmp_dict:
            self.device_t_dict['device_state_id'] = 1
            self.device_t_dict['sysname'] = self.pysnmp_dict['sysname']
        elif self.pysnmp_dict:
            self.device_t_dict['device_state_id'] = 3
            self.device_t_dict['sysname'] = self.pysnmp_dict['sysname']
        elif self.icmp_state_dict:
            self.device_t_dict['device_state_id'] = 4
        else:
            self.device_t_dict['device_state_id'] = 2
        try:
            # 处理返回给devicedetail表的数据
            if self.pysnmp_dict:

                # 定义字符串接收 处理后的结果
                net_area_data = ''
                device_type_data = ''
                device_location_data = ''
                # 取出sysname，并以 '_' 分割
                split_data = self.pysnmp_dict['sysname'].split('_')
                # print(split_data)
                if not split_data or len(split_data) < 5:
                    self.pysnmp_dict.pop('sysname')
                    self.deivcedetail_t_dict = self.pysnmp_dict
                    self.deivcelocation_t_dict['device_location'] = ''
                else:
                    # 判断网络区域
                    if split_data[-3] == 'JCW':
                        net_area_data = '基础网'
                    elif split_data[-4] == 'JCW':
                        net_area_data = '基础网'
                    else:
                        net_area_data = split_data[2]

                    # 判断设备类型
                    if split_data[-2] == 'SW':
                        device_type_data = '核心交换机'
                    elif split_data[-2] == 'AGGE':
                        device_type_data = '汇聚交换机'
                    elif split_data[-2] == 'ACC':
                        device_type_data = '接入交换机'
                    elif split_data[-2] == 'FW':
                        device_type_data = '防火墙'
                    elif split_data[-2] == 'ROUTER':
                        device_type_data = '路由器'
                    elif split_data[-2] == 'WLC':
                        device_type_data = '无线控制器'
                    else:
                        device_type_data = split_data[-2]
                    # print('设备类型是：' + device_type_data + split_data[-2])

                    # 判断设备位置
                    if split_data[1][0].isdigit():
                        device_location_data = '信息机房' + split_data[1]
                    elif split_data[1].startswith('RDSBJ-'):
                        # 此处还要增加一个判断，有些位置 有-1
                        # 不能只获取到14 后面的 1 也要添加进来
                        device_location_data = '弱电设备间' + split_data[
                            1].split('-', 1)[1]
                    elif split_data[1].startswith('RDJ-'):
                        device_location_data = '弱电间' + split_data[1].split(
                            '-')[1]
                    else:
                        device_location_data = split_data[1]

                    self.pysnmp_dict['net_area'] = net_area_data
                    self.pysnmp_dict['device_type'] = device_type_data

                    # 确定返回的字典
                    self.pysnmp_dict.pop('sysname')
                    self.deivcedetail_t_dict = self.pysnmp_dict
                    self.deivcelocation_t_dict[
                        'device_location'] = device_location_data
        except Exception as e:
            print(str(e) + self.pysnmp_dict['sysname'])

    def run(self, mgmt_ip, community_data):
        self.icmp_polling(mgmt_ip)
        self.do_pysnmp(mgmt_ip, community_data)
        self.res_process()
        return self.device_t_dict, self.deivcedetail_t_dict, self.deivcelocation_t_dict


def run(polling_dict):
    mgmt_ip = polling_dict['mgmt_ip']
    community_data = polling_dict['community_data']

    obj = Polling()
    res1, res2, res3 = obj.run(mgmt_ip, community_data)

    return res1, res2, res3


if __name__ == '__main__':
    obj = Polling()
    res1, res2, res3 = obj.run('172.31.100.104', 'public')
    print(res1)
    print('-----------')
    print(res2)
    print('-----------')
    print(res3)
    print('-----------')    
