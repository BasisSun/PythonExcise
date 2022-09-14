# coding=UTF8
from flask import Flask, request
import json
app = Flask(__name__)


@app.route('/', methods=['GET', ])
def index():
    # return {
    #     "msg": "success",
    #     "data": "welcome to use flask."
    # }
    return 'hello word!'

# 邦文接口
@app.route('/type=getUserInfoByCardNumForGLC&cardNum=9F4EC424', methods=['GET', ])
def CardLogin():
    return {
        "birthday": "1953-12-22",
        "sex": 2,
        "risk": 0,
        "username": "anni",
        "subver": 0,
        "unitprice": 0.0,
        "addver": 0,
        "error": "",
        "height": 163.0,
        "mainver": 0,
        "weight": 52,
        "userid": 6,
        "vicever": 0,
        "hrrest": 0,
        "ntrname": "张三"}

    #     "msg": "success",
    #     "data": "welcome to use flask."
    
#博谐接口
@app.route('/userinfo', methods=['GET', ])
def BoxieLogin():

    user = request.args.get('username')
    print(user)
    return {
        "birthday": "1994-12-22",
        "sex": 2,
        "risk": 0,
        "username": "anni",
        "subver": 0,
        "unitprice": 0.0,
        "addver": 0,
        "error": "",
        "height": 163.0,
        "mainver": 0,
        "weight": 52,
        "userid": 6,
        "vicever": 0,
        "hrrest": 0,
        "ntrname": "张三"}

    #     "msg": "success",
    #     "data": "welcome to use flask."

#邦文上传
@app.route('/tph/service/cycle/test.json', methods=['POST'])
def PrintPost():
    if request.method == 'POST':
        data = request.get_data()
        print(data)
        json_data = json.loads(data.decode("utf-8"))
        print(json_data)
        return {
            "msg": "success",
            "value": "0",
            "code": 200,
            "state": "1"
        }


if __name__ == '__main__':
    # '0.0.0.0'代表在本地服务器上并以局域网形式访问
    app.run(host='0.0.0.0', port=5000)
