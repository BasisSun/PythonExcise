def fib(n):    # 定义到 n 的斐波那契数列
    a, b = 0, 1
    while b < n:
        print(b, end=' ')
        a, b = b, a+b
    print()

def fib2(n): # 返回到 n 的斐波那契数列
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a+b
    return result
	
def minidig(b):
	arr=[10**x for x in range(1,6)]
	arr1=[]
	arr1.append(b%10)
	for i in range(0,4):
		if arr[i]<b:
			dig=b%arr[i+1]//arr[i]
			arr1.append(dig)
	#print("数据:",arr1)
	numofDit=len(arr)
	arr1.sort()
	#print("排序后数据:",arr1)
	for k in arr1:
		if k!=0:
			FirN=k
			arr1.remove(k)
			arr1.insert(0,k)
			break
	#print("最小整数据:",arr1)
	return arr1