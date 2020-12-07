from tkinter import *
import math as m

root = Tk()

w=Canvas(root,width=200,height=100)

w.pack()

def xjie():
	w.create_line(0,0,200,100,fill="green",width=3)
	w.create_line(200,0,0,100,fill="green",width=3)
	w.create_rectangle(40,20,160,80,fill="green")
	w.create_rectangle(65,35,135,65,fill="green")
	w.create_text(100,50,text="FishC",fill="pink")
	
def oval():
	w.create_rectangle(40,20,160,80,dash=(4,4))
	oval=w.create_oval(40,20,160,80,fill="pink")
	w.create_text(100,50,text="FishC")
	w.coords(oval,70,20,130,80)
	
def Wujiaoxing():
	center_x=100
	center_y=50
	r=50
	points=[center_x-int(r*m.sin(2*m.pi/5)), center_y-(r*m.cos(2*m.pi/5)),
			center_x+int(r*m.sin(2*m.pi/5)), center_y-(r*m.cos(2*m.pi/5)),
			center_x-int(r*m.sin(m.pi/5)), center_y+(r*m.sin(m.pi/5)),
			center_x, center_y-r,
			center_x+int(r*m.sin(m.pi/5)), center_y+(r*m.sin(m.pi/5))]
	w.create_polygon(points,outline="green",fill="yellow")

#画一条黄色的横线
line1=w.create_line(0,50,200,50,fill="yellow")
#画一条红色的横线
line2=w.create_line(100,0,100,100,fill="red",dash=(4,4))

#中间画一个蓝色的矩形
rec1=w.create_rectangle(50,25,150,75,fill="blue")

w.coords(line1,0,25,200,25)
w.itemconfig(rec1,fill="purple")

Button(root,text="删除全部",command=(lambda x=ALL:w.delete(x))).pack()
Button(root,text="换个图像",command=xjie).pack()
Button(root,text="换个椭圆",command=oval).pack()
Button(root,text="五角形",command=Wujiaoxing).pack()



mainloop()