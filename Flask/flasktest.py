# coding=gbk
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

# 邦文登录


@app.route('/type=getUserInfoByCardNumForGLC&cardNum=9F4EC424', methods=['GET', ])
def CardLogin():
    return {
        "birthday": "1953-12-22",
        "sex": 2,
        "risk": 0,
        "username": "洪根兄",
        "subver": 0,
        "unitprice": 0.0,
        "addver": 0,
        "error": "",
        "height": 163.0,
        "mainver": 0,
        "weight": 52.6,
        "userid": 6,
        "vicever": 0,
        "hrrest": 0,
        "ntrname": "洪根兄"}

    #     "msg": "success",
    #     "data": "welcome to use flask."


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
    # '0.0.0.0'的目的是允许别的设备通过网络访问
    app.run(host='0.0.0.0', port=5000)
