import pyautogui,time,os

time.sleep(5)
# im = pyautogui.screenshot()

# print(im.getpixel((0, 0)))

# print(im.getpixel((50, 200)))

#图像识别
os.chdir('C:\\Users\\Administrator\\Desktop\\CATIA临时文件\\Phython0\\GUI')
time.sleep(5)

startTime=time.time()

CaaWeb=pyautogui.locateOnScreen('CAAWeb.png')

endTime=time.time()

print("it cost %s s to search" % round(endTime-startTime,2))

if CaaWeb != None:
	print(CaaWeb)
	CAAIconXY=pyautogui.center(CaaWeb)
	pyautogui.doubleClick(CAAIconXY)
else:
	print("There is no matching icon on the desktop")

