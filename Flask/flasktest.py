#coding=gbk
from flask import Flask
app = Flask(__name__)


@app.route('/', methods=['GET', ])
def index():
    # return {
    #     "msg": "success",
    #     "data": "welcome to use flask."
    # }
    return 'hello word!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # '0.0.0.0'��Ŀ������������豸ͨ���������