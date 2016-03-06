#!/usr/bin/python

from flask import Flask, render_template, request, Response
from functools import wraps
import requests
from requests.auth import HTTPBasicAuth
import json

app = Flask(__name__, static_url_path="")


def check_auth(username, password):
    return username == 'treeuser' and password == 'raspberrypi'

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route("/", methods=['GET'])
@requires_auth
def main():
    return render_template('index.html')


@app.route("/worker/<title>", methods=['GET'])
@requires_auth
def worker(title):
    url = 'http://api.fisc.us:8080/pwmtree/api/tasks'
    headers = {'Content-Type': 'application/json'}
    data = '{"title":"' + title + '"}'
    response = requests.post(url, auth=HTTPBasicAuth('pi', 'python'), headers=headers, data=data)
    
    return title


@app.route("/worker/dimmer/<int:value>", methods=['GET'])
@requires_auth
def dimmer(value):
    url = 'http://api.fisc.us:8080/pwmtree/api/tasks'
    headers = {'Content-Type': 'application/json'}
    data = '{"title":"dimmer","value":""' + value + '""}'
    response = requests.post(url, auth=HTTPBasicAuth('pi', 'python'), headers=headers, data=data)
    
    return value


if __name__ == '__main__':
    app.run(host = "", port = 8081, debug = True)
