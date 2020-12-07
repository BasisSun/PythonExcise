import EMail

if __name__=='__main__':
	my_sender='sungj66@qq.com'    # 发件人邮箱账号
	my_pass = 'sun20320'              # 发件人邮箱密码
	my_objmail=input("请输入对方的邮箱号，如果有多个用英文“;”隔开：")
	my_user=[]
	if my_objmail=="":
		my_user=['sungj66@139.com']      # 收件人邮箱账号，我这边发送给自己
	else:
		my_user=my_objmail.split(';')
	my_text="""
你好: 
\t这是一封测试邮件。
\t此致
敬礼！
\t\t\t\t\t孙根基"""
	ret=EMail.mail(my_sender,my_pass,my_user,my_text)
	if ret:
		print("邮件发送成功")
	else:
		print("邮件发送失败")