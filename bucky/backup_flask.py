from flask import Flask, jsonify, request
import subprocess
from flask_cors import CORS, cross_origin
import json
import requests

old_kills_dict = {
                    "bucky" : 0
                }
RATE_LIMIT_SLEEP = 60
UPDATE_SLEEP = 20
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/test')
@cross_origin()
def test():
    res = requests.get('http://api.open-notify.org/astros.json')
    return res.text

@app.route('/buckyjson')
@cross_origin()
def filegrab():
    f = open('/home/GavieData/mysite/data.json')
    data = json.load(f)
    return data


if __name__ == '__main__':
    app.run(debug=True)
