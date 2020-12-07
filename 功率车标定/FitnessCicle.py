import numpy as np

f = open("D:/fitnesscicle.txt", "r")
str0 = f.readlines() #读取三组数据值
#print(str)
str_x = str0[0].rstrip('\n').split(',')#读取实际AD值
str_y = str0[1].rstrip('\n').split(',')#读取实际功率

str_z = str0[2].rstrip('\n').split(',')#读取目标功率

#将字符串列表转化为数字列表
x = [float(i) for i in str_x]
y = [float(j) for j in str_y]
z = [float(k) for k in str_z]

print(x)
print(y)
print(z)

# 关闭打开的文件
f.close()

#三次多项式拟合
z1 = np.polyfit(x, y, 3)
p1 = np.poly1d(z1)#将系数代入方程，得到函式p1
print("y=   ",p1)#多项式方程

#求取第i个目标功率时的目标函数
def solve_function(x0,i_Z1,i_z,i):
    return i_Z1[0]*(x0**3)+i_Z1[1]*(x0**2)+i_Z1[2]*x0+i_Z1[3]-i_z[i]

# 二分法求根
def dichotomy(left, right,eps,i_Z1,i_z,i):
    middle = (left+right)/2
    count=0 # 统计迭代次数
    while abs(right-left)>eps:
        middle = (left+right)/2
        if solve_function(left,i_Z1,i_z,i)*solve_function(middle,i_Z1,i_z,i)<=0:
            right=middle
        else:
            left=middle
        count=count+1
    return middle


#计算AD值的上下限（取值范围）
Lim_L = 0
Lim_R = max(x)*1.1

#主程序
pow_ad = []
for i in range(len(z)):
    pow_ad_i = round(dichotomy(Lim_L, Lim_R, 0.05 , z1 , z ,i),1)
    pow_ad.append(str(pow_ad_i))

#将结果写入文件
str_pow_ad = ','.join(pow_ad)
str_pow_ad ="目标功率档位划分为："+ str_pow_ad+'\n'
f = open("D:/fitnesscicle.txt", "a")
f.write(str_pow_ad)
f.close()