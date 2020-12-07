tableData = [['apples', 'oranges', 'cherries', 'banana'],
			['Alice', 'Bob', 'Carol', 'David'],
			['dogs', 'cats', 'moose', 'goose']]

for i in range(4):
	ArrLen=[]
	for j in range(3):
		len0=len( tableData[j][i])
		ArrLen.append(len0)
	
	MaxLen=max(ArrLen)
	
	for k in range(3):
		tableData[k][i]=tableData[k][i].ljust(MaxLen,' ')
	
for i in range(3):
	TempData="  ".join(tableData[i])
	print(TempData)
