#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import os


class Notifier:
    """通知模块，用于发送消息通知"""
    
    def __init__(self, webhook_urls):
        """
        初始化通知器实例
        
        Args:
            webhook_urls: webhook URL的列表或字符串
        """
        if isinstance(webhook_urls, str):
            self.webhook_urls = [webhook_urls]
        else:
            self.webhook_urls = webhook_urls
        
        # 获取系统代理设置
        self.proxies = self._get_system_proxies()
    
    def _get_system_proxies(self):
        """
        获取系统代理设置
        
        Returns:
            dict: 包含http和https代理的字典，如果没有代理则返回空字典
        """
        proxies = {}
        # 检查环境变量中的代理设置
        http_proxy = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
        https_proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
        
        if http_proxy:
            proxies['http'] = http_proxy
        if https_proxy:
            proxies['https'] = https_proxy
            
        # 如果没有在环境变量中找到代理，则尝试使用requests的系统代理检测
        if not proxies:
            try:
                system_proxies = requests.utils.get_environ_proxies('')
                if system_proxies:
                    proxies = system_proxies
            except Exception as e:
                print(f"获取系统代理时发生错误: {str(e)}")
                
        return proxies
    
    def send_text(self, content, mentioned_list=None, mentioned_mobile_list=None):
        """
        发送文本消息
        
        Args:
            content: 消息内容
            mentioned_list: 要@的成员ID列表
            mentioned_mobile_list: 要@的成员手机号列表
            
        Returns:
            bool: 是否发送成功
        """
        data = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": mentioned_list or [],
                "mentioned_mobile_list": mentioned_mobile_list or [],
            },
        }
        return self._send(data)
    
    def _send(self, data, webhook_url=None):
        """
        发送消息到指定的webhook URL
        
        Args:
            data: 要发送的消息数据
            webhook_url: 要发送的webhook URL，如果不指定，则发送到所有webhook URLs
            
        Returns:
            bool: 是否发送成功
        """
        if webhook_url is None:
            webhooks = self.webhook_urls
        else:
            webhooks = [webhook_url]

        for webhook in webhooks:
            try:
                headers = {"Content-Type": "application/json"}
                # 使用系统代理发送请求
                response = requests.post(
                    webhook, 
                    headers=headers, 
                    data=json.dumps(data),
                    proxies=self.proxies if self.proxies else None  # 如果有代理则使用
                )
                if response.status_code != 200 or response.json()["errcode"] != 0:
                    print(f"发送消息失败: {response.json()}")
                    return False
            except Exception as e:
                print(f"发送消息过程中发生错误: {str(e)}")
                return False
        return True


# 使用示例
if __name__ == "__main__":
    # 初始化通知器
    notifier = Notifier(webhook_urls=["https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"])
    
    # 发送即时消息
    success = notifier.send_text("这是一条测试消息")
    print(f"消息发送{'成功' if success else '失败'}")
    # 打印当前使用的代理
    print(f"当前系统代理设置: {notifier.proxies}") 