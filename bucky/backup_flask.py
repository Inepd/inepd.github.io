from flask import Flask, jsonify, request
import subprocess
from flask_cors import CORS, cross_origin
import json
import requests

count = 1
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/inepd-bucky')
@cross_origin()
def inepd_bucky():
    def get_kills(url):
        res = requests.get(url)
        html = res.text
        #cuts from first </p>
        index1 = html.find("</script>") + len("</script>")
        removed1 = html[index1:]
        #cuts from second </p>
        index2 = removed1.find("</script>") + len("</script>")
        removed2 = removed1[index2:]
        #cuts from third </p>
        index3 = removed2.find("</script>") + len("</script>")
        removed3 = removed2[index3:]
        #cuts from fourth </p>
        index4 = removed3.find("</script>") + len("</script>")
        removed4 = removed3[index4:]
        #cuts from fifth </p>
        index5 = removed4.find("<script>") + len("<script>")
        removed5 = removed4[index5:]

        index6 = removed5.find('</script>')
        removed6 = removed5[len('"window.__INITIAL_STATE__ ='):index6]

        json_data = json.loads(removed6)

        counter = 0
        for i in json_data['stats']['segments']:
            if json_data['stats']['segments'][counter]['attributes']['key'] == 'bucky':
                return json_data['stats']['segments'][counter]['stats']['kills']['value']

            counter += 1

    comp_kills = get_kills('https://tracker.gg/valorant/profile/riot/Inepd%23bucky/weapons?season=all&playlist=competitive')
    unrated_kills = get_kills('https://tracker.gg/valorant/profile/riot/Inepd%23bucky/weapons?season=all&playlist=unrated')
    swift_kills = get_kills('https://tracker.gg/valorant/profile/riot/Inepd%23bucky/weapons?season=all&playlist=swiftplay')

    data_dict = {
                    "bucky" : comp_kills + unrated_kills + swift_kills
                }
    return jsonify(data_dict)

@app.route('/test')
@cross_origin()
def test():
    res = requests.get('http://api.open-notify.org/astros.json')
    return res.text


if __name__ == '__main__':
    app.run(debug=True)
