import win32serviceutil 

import win32service 

import win32event 

import os

import socket

class PythonService(win32serviceutil.ServiceFramework): 

    #服务名

    _svc_name_ = "weater"

    #服务显示名称

    _svc_display_name_ = "weater"

    #服务描述

    _svc_description_ = "天气服务"

 

    def __init__(self, args): 

        win32serviceutil.ServiceFramework.__init__(self, args) 

        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

        self.isAlive = True

    def SvcDoRun(self):

        import time

        while self.isAlive:

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            result = sock.connect_ex(('127.0.0.1', 80))

            if result != 0:

                os.popen('python D:\\test\\web_Django\\we\\manage.py runserver 0.0.0.0:80')

                time.sleep(8)

            sock.close()

            time.sleep(20)

            

    def SvcStop(self): 

        # 先告诉SCM停止这个过程 

        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING) 

        # 设置事件 

        win32event.SetEvent(self.hWaitStop) 

        self.isAlive = False

 

if __name__=='__main__': 

    win32serviceutil.HandleCommandLine(PythonService)