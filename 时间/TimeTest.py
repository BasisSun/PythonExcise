import time

def calcProd(): # Calculate the product of the first 100,000 numbers.
	product = 1
	for i in range(1, 10000):
		product = product * i
	return product
	
startTime = time.time()
prod = calcProd()
endTime = time.time()
print('The result is %s digits long.' % (len(str(prod))))
print('Took %s seconds to calculate.' % round((endTime - startTime),3))

# for i in range(3):
	# print('Tick')
	# time.sleep(1)
	# print('Tock')
	# time.sleep(1)

time.sleep(30)