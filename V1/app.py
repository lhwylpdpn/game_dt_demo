# -*- coding:utf-8 -*-
"""
@author HU
"""
import json
import traceback
from flask import request
from flask import Flask, Response
from buildpatrol import BuildPatrol
from unit_test import test_tool

conf = {
    "DEBUG": True
}

app = Flask("game-dt", static_url_path='/static', static_folder='static/dist' )

@app.route('/')
def hello():
    return "Server is running..."


@app.route('/create-patrol', methods=['POST', 'GET'])
def create_patral():
    data = request.get_data()
    state = BuildPatrol(json.loads(data))
    return test_tool(state=state)


@app.route('/favicon.ico')
def get_fav():
    return app.send_static_file('favicon.ico')


@app.errorhandler(Exception)
def handler_error(e):
    if getattr(conf, 'DEBUG', False):
        resp = traceback.format_exception(type(e), e, e.__traceback__)
    else:
        resp = "Things go wrong."
    return Response(response=resp, status=500)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7001, debug=getattr(conf, 'DEBUG', False), use_reloader=False)
