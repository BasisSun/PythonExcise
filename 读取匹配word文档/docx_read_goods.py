from docx import Document
from docx.shared import Inches

#获取程序所在文件夹所有文件
def list_all_files():
    import os
    _files = []
    list = os.listdir('./') #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
           path = os.path.join('./',list[i])
           if os.path.isdir(path):
              _files.extend(list_all_files())
           if os.path.isfile(path):
              _files.append(path)
    return _files

 
if __name__ == '__main__':

    #检索词
    a=input("请输入检索词：")

    #获取程序所在文件夹所有文件
    list_files = list_all_files()

    for file in list_files:
        filename = str(file)
        if filename.find("采购链接")!=-1 and filename.find(".doc")!=-1 and filename.find("~$") == -1:
            print("*********************************************************")
            print(filename,'\n')

            document = Document(file)  #打开文件demo.docx

            tables = document.tables #获取文件中的表格集
            table = tables[0  ]#获取文件中的第一个表格
            for i in range(1,len(table.rows)):#从表格第二行开始循环读取表格数据
                name = table.cell(i,1).text

                if name.find(a) != -1 :
                    result = table.cell(i,0).text+'\n'+name+'\n' + "链接："+table.cell(i,3).text+'\n'
                    #cell(i,0)表示第(i+1)行第1列数据，以此类推
                    print(result)
                    
            print("*********************************************************")

    
