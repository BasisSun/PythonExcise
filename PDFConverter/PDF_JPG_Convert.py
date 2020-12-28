import fitz
import glob
import os
from PIL import Image


def pic2pdf():
    doc = fitz.open()
    list_img = glob.glob("*.jpg")

    if(len(list_img)==0):
        list_img = glob.glob("*.jpeg")
        if(len(list_img)==0):
            list_img = glob.glob("*.png")
            if(len(list_img)==0):
                input("本目录下未找到有效图片文件，支持.jpg，.jpeg，.png")
                return

    for img in sorted(list_img):  # 读取图片，确保按文件名排序
        print(img)
        imgdoc = fitz.open(img)                 # 打开图片
        pdfbytes = imgdoc.convertToPDF()        # 使用图片创建单页的 PDF
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)                   # 将当前页插入文档

    if os.path.exists("合成结果.pdf"):
        os.remove("合成结果.pdf")

    doc.save("合成结果.pdf")                   # 保存pdf文件
    doc.close()


def rightinput(desc):
    flag = True
    while(flag):
        instr = input(desc)
        try:
            intnum = eval(instr)
            if type(intnum) == int:
                flag = False
        except:
            print('请输入正整数！')
            pass
    return intnum


if __name__ == '__main__':
    a = int(input("请输入要进行的操作：\n1：图片（jpg）转PDF\n2：PDF转图片\n"))

    if(a == 1):
        pic2pdf()

    elif(a == 2):
        pdffile = glob.glob("*.pdf")[0]  # 只选第一个
        doc = fitz.open(pdffile)

        flag = rightinput("输入：1：全部页面；2：选择页面\t")
        if flag == 1:
            strat = 0
            totaling = doc.pageCount
        else:
            strat = rightinput('输入起始页面：') - 1
            totaling = rightinput('输入结束页面：')

        for pg in range(strat, totaling):
            page = doc[pg]
            zoom = int(150)
            rotate = int(0)
            trans = fitz.Matrix(zoom / 100.0, zoom / 100.0).preRotate(rotate)
            pm = page.getPixmap(matrix=trans, alpha=False)

            pm.writePNG('%s.png' % str(pg+1))

        pngfiles = glob.glob("*.png")  # 全部转换成JPG

        for pngfile in pngfiles:
            img = Image.open(pngfile)
            str = pngfile.rsplit(".", 1)
            output_img_path = str[0] + ".jpg"
            print(output_img_path)
            img.save(output_img_path)
            os.remove(pngfile)  # 删除PNG文件
