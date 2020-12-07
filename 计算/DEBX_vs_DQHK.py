f=int(input("请输入总本金："))
a=float(input("请输入等额本息利率(%)"))/100
b=float(input("请输入全额还款利率（%）"))/100
c=float(input("请输入同期货币基金利率:(%)"))/100
Time=int(input("请输入时间：（月）"))

Re_per_mon = f*1.0/Time

Re_Gross = 0

Lx0=0
Lx1=0

Lx1=f*b/365.0*30*Time

for i in range(Time):
    Lx0+=f*a/365.0*30.0
    Lx0+=Re_Gross*c/365.0*30.0
    f-=Re_per_mon
    Re_Gross+=Re_per_mon


print("使用等额本息，你将获得",Lx0,"元")
print("使用全额还款，你将获得",Lx1,"元")
