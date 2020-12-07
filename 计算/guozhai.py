
Benjin=float(input("请输入本金额度："))
days=0

while(1):
	days=int(input("请输入逆回购天数："))
	if days not in [1,2,3,4,7,14,28,91,182]:
		print("没有这种天数的品种，请输入1,2,3,4,7,14,28,91,182中的一种")
	else:
		break


if(days in range(1,5)):
	ShXuFL=0.00001*days
elif(days==7):
	ShXuFL=0.00005
elif(days==14):
	ShXuFL=0.0001
elif(days==28):
	ShXuFL=0.0002
elif(days==91 or days==182):
	ShXuFL=0.0003
	
ExtraDays=int(input("请输入实际计息天数："))
days=ExtraDays

JijinLV=float(input("请输入同期货币基金利率："))

ActualDays=days+3 #实际占用天数

JijinLX=Benjin*JijinLV/365*ActualDays
print("基金利息："+str(JijinLX))

GuoZhLX=0
GuozhaiLV=JijinLV;#从利率相等开始递增

while (GuozhaiLV<3):
	GuoZhLX=Benjin*GuozhaiLV/365*days-Benjin*ShXuFL
	print("国债利率：{} 国债利息：{} （已经扣掉手续费{}）".format(round(GuozhaiLV,3),round(GuoZhLX,3),round(Benjin*ShXuFL,1)))
	if (GuoZhLX>JijinLX):
		print("当国债逆回购的利率大于"+str(GuozhaiLV)+"时，买国债才划算")
		break
	else:
		GuozhaiLV+=0.001
else:
	print("300%以内是没有可能了。。")