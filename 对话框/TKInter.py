import tkinter as tk, os

os.chdir('C:\\Users\\Administrator\\Desktop\\CATIA临时文件\\Phython0\\对话框')

class App:
	def __init__(self,root):
	
		frame=tk.Frame(root)
		frame.title="优美图片"
		frame.pack(side=tk.LEFT,padx=0,pady=0)#与边框的偏移
		# self.Label = tk.Label(frame,text="下面是个按钮")
		# self.Label.pack()
		# self.hi_there = tk.Button(frame,text="打招呼",fg="blue",bg="white",command=self.say_hi)
		# self.hi_there.pack()
		# self.textLabel=tk.Label(frame,text="这是一个\n桌面快捷方式",fg="red")
		# self.textLabel.pack(side=tk.LEFT)
		# self.photo=tk.PhotoImage(file="CAAWeb.png")
		# self.imageLabel=tk.Label(frame,image=self.photo)
		# self.imageLabel.pack(side=tk.RIGHT)
		
		self.backgound=tk.PhotoImage(file="背景.png")
		self.theLabel=tk.Label(root,image=self.backgound,text="风\n之\n舞",compound=tk.CENTER,font=("华文行楷",40),fg="black")#,
		self.theLabel.pack()
	
	def say_hi(self):
		print("互联网的广大朋友们大家好，我是。。")
	
root = tk.Tk()

app=App(root)
root.mainloop()
