#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import socket
import re
import json

class ePortal:
    """安徽大学校园网自动登录类"""
    
    def __init__(self, user_account, user_password):
        """
        初始化ePortal实例
        
        Args:
            user_account: 学号
            user_password: 密码
        """
        self.user_account = user_account
        self.user_password = user_password
        self.base_url = "http://172.16.253.3:801/eportal/"
        self.login_url = f"{self.base_url}?c=Portal&a=login&callback=dr1003&login_method=1&jsVersion=3.3.2&v=1117"
        self.campus_check_url = "http://172.16.253.3/a79.htm"
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Referer": "http://172.16.253.3/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.wlan_user_ip = self.get_local_ip()
    
    def get_local_ip(self):
        """
        获取本机IP地址
        
        Returns:
            str: 本机IP地址
        """
        try:
            # 创建一个临时socket连接到一个公共IP，获取本机IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            # 如果上述方法失败，尝试其他方法
            try:
                hostname = socket.gethostname()
                ip = socket.gethostbyname(hostname)
                return ip
            except Exception as e:
                print(f"获取IP地址失败: {e}")
                return "127.0.0.1"  # 失败时返回本地回环地址
    
    def is_connected_to_campus_network(self):
        """
        检查是否已连接到校园网（但可能尚未认证）
        
        Returns:
            bool: 是否已连接到校园网
        """
        try:
            response = requests.get(self.campus_check_url, timeout=5, headers=self.headers)
            return response.status_code == 200
        except Exception:
            return False
    
    def login(self):
        """
        执行登录操作
        
        Returns:
            bool: 登录是否成功
            str: 登录结果信息
        """
        # 首先检查是否已连接到校园网
        if not self.is_connected_to_campus_network():
            return False, "尚未连接校园网"
            
        try:
            # 构建登录参数
            params = {
                "c": "Portal",
                "a": "login",
                "callback": "dr1003",
                "login_method": "1",
                "user_account": self.user_account,
                "user_password": self.user_password,
                "wlan_user_ip": self.wlan_user_ip,
                "wlan_user_ipv6": "",
                "wlan_user_mac": "000000000000",
                "wlan_ac_ip": "",
                "wlan_ac_name": "",
                "jsVersion": "3.3.2",
                "v": "1117"
            }
            
            # 发送登录请求
            response = requests.get(
                self.login_url, 
                params=params,
                headers=self.headers
            )
            
            # 处理返回结果
            if response.status_code == 200:
                # 提取JSON数据 (通常在dr1003()中)
                json_str = re.search(r'dr1003\((.*)\)', response.text)
                if json_str:
                    result = json.loads(json_str.group(1))
                    if result.get("result") == "1":
                        return True, "登录成功"
                    else:
                        return False, result.get("msg", "登录失败，未知原因")
                else:
                    return False, "登录失败，无法解析返回数据"
            else:
                return False, f"登录失败，HTTP状态码: {response.status_code}"
        
        except Exception as e:
            return False, f"登录过程中发生异常: {str(e)}"


# 使用示例
if __name__ == "__main__":
    import getpass
    
    user_account = input("请输入学号: ")
    user_password = getpass.getpass("请输入密码: ")
    
    portal = ePortal(user_account, user_password)
    success, message = portal.login()
    print(message) 