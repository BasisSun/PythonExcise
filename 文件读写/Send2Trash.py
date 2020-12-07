import send2trash,os

print(os.getcwd())

os.chdir('C:\\Users\\Administrator\\Desktop\\CATIA临时文件\\Phython0\\文件读写')

baconFile = open('bacon.txt', 'a') # creates the file
baconFile.write('Bacon is not a vegetable.')
baconFile.close()
send2trash.send2trash('bacon.txt')