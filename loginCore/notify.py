#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests


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
                response = requests.post(webhook, headers=headers, data=json.dumps(data))
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