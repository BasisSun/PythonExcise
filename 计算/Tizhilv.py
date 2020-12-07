#计算体脂率
Weight=float(input("请输入体重："))
Circ=float(input("请输入腰围："))

a=Circ*0.74
b=Weight*0.082+44.74

Tizhilv=(a-b)/Weight

print("您的体脂率是：",Tizhilv)

input("Prease <enter>")