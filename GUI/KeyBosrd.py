import pyautogui,time

time.sleep(5)

pyautogui.click(100, 100); 
pyautogui.typewrite('Hello world!',0.25)

pyautogui.keyDown('shift');
pyautogui.press('4'); 
pyautogui.keyUp('shift')

print("Plesse select text!")
for i in range(5):
	print(5-i);
	time.sleep(1);

pyautogui.hotkey('ctrl', 'c')

print("Plesse put down the cursor!")
for i in range(5):
	print(5-i);
	time.sleep(1);

pyautogui.hotkey('ctrl', 'v')