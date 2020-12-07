import os
from tkinter import *

os.chdir('E:\\Python0\\对话框')

def callback():
	var.set("哈哈哈")
	

root=Tk()
frame1=LabelFrame(root,text="猜猜看",padx=10,pady=10)#内部到外框距离
frame2=Frame(root)

var=StringVar()

var.set("下面是句话")

textLabel=Label(frame1,textvariable=var,justify=LEFT)
textLabel.pack(side=LEFT)

photo =PhotoImage(file="CAAWeb.png")
imgLabel=Label(frame1,image=photo)
imgLabel.pack(side=RIGHT)

theButton = Button(frame2,text="看看",command=callback)
theButton.pack()

frame1.pack(padx=10,pady=10)#外部到主窗体距离
frame2.pack(padx=10,pady=10)

mainloop()
