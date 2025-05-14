import sys
import os
import json
import subprocess

from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from qfluentwidgets import LineEdit, PushButton, PrimaryPushButton, ToolButton, FluentIcon as FIF, InfoBar, InfoBarPosition, MessageBox

class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.loadConfig()
        self.bindEvents()

    def setupUi(self):
        # 设置窗口标题和大小
        self.setWindowTitle('AHU校园网自动登录程序')
        self.resize(400, 300)
        
        # 主布局
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(30, 30, 30, 30)
        self.mainLayout.setSpacing(15)
        
        # 学号输入框
        self.studentIdLayout = QVBoxLayout()
        self.studentIdLabel = QLabel('学号')
        self.studentIdLineEdit = LineEdit(self)
        self.studentIdLineEdit.setPlaceholderText('请输入学号')
        self.studentIdLayout.addWidget(self.studentIdLabel)
        self.studentIdLayout.addWidget(self.studentIdLineEdit)
        
        # 密码输入框
        self.passwordLayout = QVBoxLayout()
        self.passwordLabel = QLabel('密码')
        self.passwordLineEdit = LineEdit(self)
        self.passwordLineEdit.setPlaceholderText('请输入密码')
        self.passwordLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordLayout.addWidget(self.passwordLabel)
        self.passwordLayout.addWidget(self.passwordLineEdit)
        
        # 企微webhook输入框
        self.webhookLayout = QHBoxLayout()
        self.webhookLabelLayout = QHBoxLayout()
        self.webhookLabel = QLabel('企微webhook')
        self.infoButton = ToolButton(FIF.INFO, self)
        self.infoButton.setIconSize(QSize(16, 16))
        self.infoButton.clicked.connect(self.openWebhookHelp)
        self.webhookLabelLayout.addWidget(self.webhookLabel)
        self.webhookLabelLayout.addWidget(self.infoButton)
        self.webhookLabelLayout.addStretch(1)
        
        self.webhookInputLayout = QVBoxLayout()
        self.webhookInputLayout.addLayout(self.webhookLabelLayout)
        self.webhookLineEdit = LineEdit(self)
        self.webhookLineEdit.setPlaceholderText('请输入企微webhook（可不填）')
        self.webhookInputLayout.addWidget(self.webhookLineEdit)
        
        # 按钮布局
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(10)
        
        # 注册计划按钮 - 使用PrimaryPushButton，蓝色风格
        self.registerButton = PrimaryPushButton('注册计划', self)
        
        # 卸载计划按钮 - 使用普通PushButton
        self.uninstallButton = PushButton('卸载计划', self)
        
        self.buttonLayout.addWidget(self.registerButton)
        self.buttonLayout.addWidget(self.uninstallButton)
        
        # 底部信息
        self.footerLayout = QHBoxLayout()
        self.footerLabel = QLabel('由<a href="https://github.com/biubush">biubush</a>开发，开源于<a href="https://github.com/biubush/AutoNet4AHU">github</a>')
        self.footerLabel.setOpenExternalLinks(True)
        self.footerLabel.setAlignment(Qt.AlignCenter)
        self.footerLayout.addWidget(self.footerLabel)
        
        # 添加到主布局
        self.mainLayout.addLayout(self.studentIdLayout)
        self.mainLayout.addLayout(self.passwordLayout)
        self.mainLayout.addLayout(self.webhookInputLayout)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.buttonLayout)
        self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(self.footerLayout)
        
        # 设置样式
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: 'Segoe UI', 'Microsoft YaHei';
            }
            QLabel {
                font-size: 14px;
            }
        """)

    def openWebhookHelp(self):
        # 打开企业微信webhook帮助文档URL
        QDesktopServices.openUrl(QUrl("https://developer.work.weixin.qq.com/document/path/91770"))
    
    def loadConfig(self):
        # 加载配置文件
        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.studentIdLineEdit.setText(config.get('student_id', ''))
                    self.passwordLineEdit.setText(config.get('password', ''))
                    
                    # 如果webhook_urls非空，则使用第一个URL
                    webhook_urls = config.get('webhook_urls', [])
                    if webhook_urls and len(webhook_urls) > 0:
                        self.webhookLineEdit.setText(webhook_urls[0])
        except Exception as e:
            self.showErrorMessage('加载配置失败', str(e))
    
    def saveConfig(self):
        # 保存配置文件
        student_id = self.studentIdLineEdit.text().strip()
        password = self.passwordLineEdit.text().strip()
        webhook_url = self.webhookLineEdit.text().strip()
        
        webhook_urls = []
        if webhook_url:
            webhook_urls.append(webhook_url)
        
        config = {
            'student_id': student_id,
            'password': password,
            'webhook_urls': webhook_urls
        }
        
        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            self.showErrorMessage('保存配置失败', str(e))
            return False
            
    def bindEvents(self):
        # 绑定按钮事件
        self.registerButton.clicked.connect(self.registerTask)
        self.uninstallButton.clicked.connect(self.uninstallTask)
    
    def registerTask(self):
        # 检查输入
        if not self.validateInput():
            return
        
        # 保存配置
        if not self.saveConfig():
            return
            
        try:
            # 确认是否注册
            title = '注册定时任务'
            content = '确定要注册自动登录定时任务吗？这将允许程序在连接网络时自动登录校园网。'
            dialog = MessageBox(title, content, self)
            
            if dialog.exec():
                current_dir = os.path.abspath(os.path.dirname(__file__))
                
                # 直接生成XML，而不是调用外部脚本
                self.createTaskXml(current_dir)
                
                # 运行批处理注册计划任务
                bat_path = os.path.join(current_dir, 'register_task.bat')
                
                # 使用subprocess调用批处理文件
                result = subprocess.run([bat_path], shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.showSuccessMessage('注册成功', '自动登录计划任务已成功注册')
                else:
                    self.showErrorMessage('注册失败', result.stderr)
        except Exception as e:
            self.showErrorMessage('注册计划任务失败', str(e))
    
    def createTaskXml(self, current_dir):
        """直接生成任务XML文件，不需要调用外部脚本"""
        import datetime
        
        # 获取模板文件和目标文件的路径
        template_path = os.path.join(current_dir, "task_template.xml")
        output_path = os.path.join(current_dir, "ahu_eportal_task.xml")
        
        # 获取VBS脚本的绝对路径
        vbs_path = os.path.join(current_dir, "ahu_eportal.vbs")
        
        # 获取当前日期时间，格式化为XML日期格式
        current_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        
        # 读取模板文件
        with open(template_path, "r", encoding="utf-16") as file:
            xml_content = file.read()
        
        # 替换占位符
        replacements = {
            "%CreationDate%": current_date,
            "%ExecutablePath%": "wscript.exe",
            "%Arguments%": f'"{vbs_path}"',
            "%WorkingDirectory%": current_dir
        }
        
        for placeholder, value in replacements.items():
            xml_content = xml_content.replace(placeholder, value)
        
        # 写入到新文件
        with open(output_path, "w", encoding="utf-16") as file:
            file.write(xml_content)
    
    def uninstallTask(self):
        try:
            # 确认是否卸载
            title = '卸载定时任务'
            content = '确定要卸载自动登录定时任务吗？卸载后将不再自动登录校园网。'
            dialog = MessageBox(title, content, self)
            
            if dialog.exec():
                # 运行批处理卸载计划任务
                current_dir = os.path.abspath(os.path.dirname(__file__))
                bat_path = os.path.join(current_dir, 'unregister_task.bat')
                
                # 使用subprocess调用批处理文件
                result = subprocess.run([bat_path], shell=True, capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.showSuccessMessage('卸载成功', '自动登录计划任务已成功卸载')
                else:
                    self.showErrorMessage('卸载失败', result.stderr)
        except Exception as e:
            self.showErrorMessage('卸载计划任务失败', str(e))
    
    def validateInput(self):
        # 验证输入
        student_id = self.studentIdLineEdit.text().strip()
        password = self.passwordLineEdit.text().strip()
        
        if not student_id:
            self.showWarningMessage('输入错误', '请输入学号')
            return False
            
        if not password:
            self.showWarningMessage('输入错误', '请输入密码')
            return False
            
        return True
    
    def showSuccessMessage(self, title, content):
        InfoBar.success(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
    
    def showWarningMessage(self, title, content):
        InfoBar.warning(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
    
    def showErrorMessage(self, title, content):
        InfoBar.error(
            title=title,
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=5000,
            parent=self
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    w = LoginWidget()
    w.show()
    
    sys.exit(app.exec()) 