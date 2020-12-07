from tkinter import *

root=Tk()
# e = Entry(root)
# e.pack(padx=10,pady=10)
# e.delete(0,END)
#e.insert(0,"默认文本...")



Label(root,text="作品:").grid(row=0)
Label(root,text="作者:").grid(row=1)

v1=StringVar()
v2=StringVar()

e1=Entry(root,textvariable=v1)

def test():
	if e1.get() == "红高粱":
		print ("有这本书！")
	else:
		print("没找到这本书！")

e2=Entry(root,textvariable=v2,validate="focusin",validatecommand=test)

e1.grid(row=0,column=1,padx=10,pady=5)
e2.grid(row=1,column=1,padx=10,pady=5)

def show():
	print("作品：《%s》" % e1.get())
	print("作者：%s" % e2.get())
	e1.delete(0,END)
	e2.delete(0,END)
	
def showinEntry():
	v1.set("XXXX")
	v2.set("YYYY")


		
Button(root,text="获取信息",width=10,command=show).grid(row=3,column=0,sticky=W,padx=10,pady=5)
Button(root,text="退出",width=10,command=showinEntry).grid(row=3,column=1,sticky=E,padx=10,pady=5)

mainloop()