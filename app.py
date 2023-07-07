from flask import Flask, Blueprint
from config import *

from router.user import userapi
from router.bill import billtask, billlist

app = Flask(__name__)

app.config.from_object(__name__)

app.register_blueprint(userapi)
app.register_blueprint(billtask)
app.register_blueprint(billlist)


@app.route('/')
def index():
    return 'index'


if __name__ == '__main__':
    app.run(debug=True)
