#coding:utf8
import UserState
import json
from flask import Flask
from flask import _app_ctx_stack
from flask import request

import MySQLdb

DATABASE = 'UserMatch'
PASSWORD = 'badperson3'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'dbConnect'):
        myCon = MySQLdb.connect(host='localhost', passwd=app.config['PASSWORD'], db=app.config['DATABASE'], user='root', charset='utf8')
        top.dbConnect = myCon
    return top.dbConnect

@app.teardown_appcontext
def closeConnect(exception):
    top = _app_ctx_stack.top
    if hasattr(top, 'dbConnect'):
        top.dbConnect.close()

@app.route("/findAMatch")
def findAMatch():
    myCon = get_db()
    uid = int(request.args['uid'])
    score = int(request.args['score'])
    scoreOff = int(request.args['scoreOff'])

    uid = UserState.findAMatch(myCon, uid, score, scoreOff)
    return json.dumps(dict(uid=uid))

if __name__ == '__main__':
    app.run()
