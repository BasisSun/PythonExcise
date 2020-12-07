import re

xmasRegex = re.compile(r'\d+\s\w+')
resultTable = xmasRegex.findall("12 drummers, 11 pipers, 10 lords, 9 ladies, 8 maids, 7 swans, 6 geese, 5 rings, 4 birds, 3 hens, 2 doves, 1 partridge")

print(resultTable)

beginsWithHello = re.compile(r'^Hello')
Result=beginsWithHello.search('Hello world!')
print(Result)
Result=beginsWithHello.search('He said hello.')
print(Result)

#替换
agentNamesRegex = re.compile(r'Agent (\w)\w*')#r'Agent (\w)\w*')
Result0=agentNamesRegex.sub(r'\1****', 'Agent Alice told Agent Carol that Agent Eve knew Agent Bob was a double agent.')
print(Result0)

result=re.search(r'\d*',"192.168.0.6")
print(result.group())