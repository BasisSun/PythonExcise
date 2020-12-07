a=int(input("请输入行数："))
for i in range(a):
	print(('*'*(2*(a-i)-1)).center(2*a+1))
