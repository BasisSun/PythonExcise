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
            "code":200
        }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # '0.0.0.0'的目的是允许别的设备通过网络访问
