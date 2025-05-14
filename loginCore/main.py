#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import argparse
from portal import ePortal
from notify import Notifier

class AutoLogin:
    """校园网自动登录入口模块"""
    
    def __init__(self, config_file="config.json"):
        """
        初始化自动登录实例
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """
        加载配置文件，如果不存在则返回空配置
        
        Returns:
            dict: 配置信息
        """
        default_config = {
            "student_id": "",
            "password": "",
            "webhook_urls": []
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                return config
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                return default_config
        else:
            return default_config
    
    def config_is_complete(self):
        """
        检查配置是否完整
        
        Returns:
            bool: 配置是否包含必要的信息
        """
        return bool(self.config.get("student_id")) and bool(self.config.get("password"))
    
    def login(self):
        """
        执行登录操作，如果配置不完整则直接退出
        
        Returns:
            bool: 登录是否成功
        """
        # 检查配置是否完整，不完整则直接退出
        if not self.config_is_complete():
            print(f"配置不完整，请配置{self.config_file}文件设置学号和密码")
            return False
        
        student_id = self.config.get("student_id")
        password = self.config.get("password")
        
        # 使用ePortal进行登录
        portal = ePortal(student_id, password)
        success, message = portal.login()
        
        # 发送通知（如果配置了webhook URLs）
        if success and self.config.get("webhook_urls"):
            self.send_notification(True, message, portal.wlan_user_ip)
        
        print(message)
        return success
    
    def send_notification(self, success, message, ip_address):
        """
        发送登录结果通知
        
        Args:
            success: 是否登录成功
            message: 登录结果消息
            ip_address: 当前IP地址
        """
        webhook_urls = self.config.get("webhook_urls", [])
        if not webhook_urls:
            return
        
        notifier = Notifier(webhook_urls)
        
        status = "成功" if success else "失败"
        content = f"校园网登录{status}通知\n\n" \
                 f"学号: {self.config.get('student_id')}\n" \
                 f"IP地址: {ip_address}\n" \
                 f"登录结果: {message}\n" \
                 f"时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        notifier.send_text(content)


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="安徽大学校园网自动登录工具")
    parser.add_argument("-c", "--config", help="指定配置文件路径", default="config.json")
    parser.add_argument("command", nargs="?", default="login", help="执行的命令，目前支持: login")
    
    return parser.parse_args()


def main():
    """程序入口点"""
    args = parse_args()
    
    # 使用指定的配置文件路径创建AutoLogin实例
    auto_login = AutoLogin(config_file=args.config)
    
    if args.command == "login":
        auto_login.login()
    else:
        print(f"未知命令: {args.command}")
        print("可用命令: login")


if __name__ == "__main__":
    main() 