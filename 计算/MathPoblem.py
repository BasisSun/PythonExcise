for i in range(100):
    for j in range(10,100):
        m=600+i
        n=j*10+1
        n3=n//100
        f=m*n3
        f1=f%10
        f3=(f%1000)//100
        if f1==5 and f3==5:
            k=m*n
            k2=(k%100)//10
            k4=(k%10000)//1000
            if k2==4 and k4==5:
                print("这两个因数分别为，{}，{}，积为{}".format(m,n,k))

input("单击任意键退出！")
