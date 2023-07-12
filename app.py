from flask import Flask, Blueprint
from flask_cors import CORS
from config import *

from router.user import userapi
from router.bill import billtask, billlist

app = Flask(__name__)

app.config.from_object(__name__)

app.register_blueprint(userapi)
app.register_blueprint(billtask)
app.register_blueprint(billlist)

CORS(app, supports_credentials=True)


@app.route('/')
def index():
    return 'index'


if __name__ == '__main__':
    app.run(debug=True)
