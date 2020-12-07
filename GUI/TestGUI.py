import pyautogui,time


width, height = pyautogui.size()
print(str(width))
print(str(height))

# for i in range(2):
	# pyautogui.moveTo(100, 100, duration=0.25)
	# pyautogui.moveTo(200, 100, duration=0.25)
	# pyautogui.moveTo(200, 200, duration=0.25)
	# pyautogui.moveTo(100, 200, duration=0.25)
	
# pyautogui.moveTo(27, 748, duration=1)

# for i in range(2):
	# pyautogui.moveRel(100, 0, duration=0.25)
	# pyautogui.moveRel(0, 100, duration=0.25)
	# pyautogui.moveRel(-100, 0, duration=0.25)
	# pyautogui.moveRel(0, -100, duration=0.25)
	
print('Press Ctrl-C to quit.')
try:
	while True:
# TODO: Get and print the mouse coordinates.
# Get and print the mouse coordinates.
		x, y = pyautogui.position()
		positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
		pixelColor = pyautogui.screenshot().getpixel((x, y))
		positionStr += ' RGB: (' + str(pixelColor[0]).rjust(3)
		positionStr += ', ' + str(pixelColor[1]).rjust(3)
		positionStr += ', ' + str(pixelColor[2]).rjust(3) + ')'
		print(positionStr)
		time.sleep(1)
except KeyboardInterrupt:
	print('\nDone.')
	

	#print('\b' * len(positionStr), end='', flush=True)