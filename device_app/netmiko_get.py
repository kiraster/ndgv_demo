from netmiko import ConnectHandler


class NetOps():

    def get_info(self, ip, username, password, display_cmd):

        try:
            device = {
                'device_type': 'hp_comware',
                'ip': ip,
                'username': username,
                'password': password,
            }

            # get return info
            with ConnectHandler(**device) as net_connect:
                res = net_connect.send_command(display_cmd)
            return res
        except Exception as e:
            print(str(e))
            return str(e) + '\n登陆失败，根据以上下提示，检查连接\nጿ ኈ ቼ ዽ ጿ ኈቼ ዽ ጿ ኈ ጿ ኈ ቼ ዽ ጿ ኈቼ ዽ ኈ ጿ ኈ ቼ ዽ ጿ ኈቼ ዽ ጿ ኈ ጿ ኈ ቼ ዽ ጿ ኈቼ ዽ ጿ ኈ ጿ ኈ ቼ ዽ ጿ ኈቼ ዽ ጿ ኈጿ ኈ ቼ ዽ ጿ ኈቼ ዽ ጿ ኈ ጿ ኈ ቼ ዽ ጿ ኈቼ ዽ ጿ ኈ ጿ ኈ ቼ ዽ ጿ ኈቼ ዽ ጿ ኈ ጿ ኈ ቼ ዽ ጿ ኈቼ ዽ ጿ ኈ ጿ ኈ ቼ ዽ ጿ ኈቼ ዽ ጿ ኈጿ ኈ ቼ ዽ ጿ ኈቼ ዽ ጿ ኈ ጿ ኈ ቼ ዽ ጿ ኈቼ ዽ ጿ ኈ ጿ ኈ ቼ ዽ ጿ ኈቼ ዽ ጿ ኈ ጿ ኈ ቼ ዽ ጿ ኈቼ ዽ ጿ ኈ ጿ ኈ ቼ ዽ ጿ ኈቼ ዽ ጿ ኈ..........ᴅᴜᴅᴜ！'
