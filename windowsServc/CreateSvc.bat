@echo.服务启动......  
@echo off  
@sc create test3 binPath= "E:\Python0\windowsServc\dist\PythonService.exe"  
@net start test3  
@sc config test3 start= AUTO  
@echo off  
@echo.启动完毕！  
@pause  