import datetime
Today=datetime.datetime.now()

HundredDays=datetime.timedelta(days=100)

print(Today+HundredDays)

print("现在的时间是：{}年{}月{}日".format(Today.strftime("%Y"),Today.strftime("%m"),Today.strftime("%d")))

print("测试%s" % 1234567)