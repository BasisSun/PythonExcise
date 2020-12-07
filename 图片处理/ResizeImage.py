import os
import time
from PIL import Image

ObjWidth=1224
ObjHeight=1632

def alter(path,object):
    s = os.listdir(path)

    print("共",len(s),"个文件")

    count = 1
    for i in s:
        print(count,'/',len(s))

        document = os.path.join(path,i)
        img = Image.open(document)
        out = img.resize((ObjWidth,ObjHeight))
        listStr = [str(int(time.time())), str(count)]
        fileName = ''.join(listStr)
        out.save(object+os.sep+'%s.jpg' % fileName)
        count = count + 1

if __name__ == "__main__":
    alter('E:\\电子书\\其他\\源目录','E:\\电子书\\其他\\目标目录')
    print("处理完成")
