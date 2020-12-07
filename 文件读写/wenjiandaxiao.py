import os

totalSize = 0
for filename in os.listdir('C:\\Users\\Administrator\\Desktop\\CATIA临时文件'):
	totalSize = totalSize + os.path.getsize(os.path.join('C:\\Users\\Administrator\\Desktop\\CATIA临时文件', filename))

MSize=round(totalSize/1024/1024,3)
print(MSize,"MB大小")

assert MSize< 200, 'File size is too large! ' + str(MSize)

