import random


f = open("C:/Users/Administrator/Desktop/foo.txt", "w")

ListX=[0.1*i for i in range(0,10)]
ListY=[0.1*i for i in range(0,10)]
print(ListX)
print(ListY)

for i in range(0,15):
	x=random.uniform(0, 1)
	y=random.uniform(0, 1)
	er=random.uniform(-0.02, 0.02) 
	z=0.5*x+1+er
	f.write("{};{}\n".format(x,z))
f.close()
