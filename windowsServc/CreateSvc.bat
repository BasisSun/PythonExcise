@echo.��������......  
@echo off  
@sc create test3 binPath= "E:\Python0\windowsServc\dist\PythonService.exe"  
@net start test3  
@sc config test3 start= AUTO  
@echo off  
@echo.������ϣ�  
@pause  