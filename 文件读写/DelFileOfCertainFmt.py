import os
import os.path
#"""获取指定目录及其子目录下的 py 文件路径说明：l 用于存储找到的 py 文件路径 get_py 函数，递归查找并存储 py 文件路径于 l"""
l=[]
def get_txt(path,l):
	fileList = os.listdir(path)   #获取path目录下所有文件
	for filename in fileList:
		pathTmp = os.path.join(path,filename)   #获取path与filename组合后的路径
		if os.path.isdir(pathTmp):   #如果是目录
			get_py(pathTmp,l)        #则递归查找
		elif filename[-4:].upper()=='.TXT':   #不是目录,则比较后缀名
			l.append(pathTmp)

ObjPath='C:\\Users\\Administrator\\Desktop\\CATIA临时文件\\Phython0\\文件读写'
get_txt(ObjPath,l)
for filepath in l:
	print(filepath)
	os.remove(filepath)