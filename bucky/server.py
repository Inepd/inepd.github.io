from urllib.request import urlopen
import requests
import json
import time

def main():
    RATE_LIMIT_SLEEP = 60
    UPDATE_SLEEP = 20
    URL = 'https://tracker.gg/valorant/profile/riot/Inepd%23bucky/weapons?playlist=competitive&season=all'
    headers = {
                "Accept-Language" : "en-US,en;q=0.5",
                "User-Agent": "Defined",
            }
    while True:
        try:
            res = requests.get(URL, headers=headers)
        except:
            print('failed')
            exit()
        if res.status_code == 429: # check that the request went through
            print('Rate Limited')
            time.sleep(RATE_LIMIT_SLEEP)
        if res.status_code == 200:

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

            with open("Output.json", "w", encoding='utf-8') as text_file:
                text_file.write(removed6)
            open_file = open(r'Output.json') #Open json into variable
            json_data = json.load(open_file) #Load json into variable

            counter = 0
            for i in json_data['stats']['segments']:
                if json_data['stats']['segments'][counter]['attributes']['key'] == 'bucky':
                    data_dict = {
                        "bucky" : json_data['stats']['segments'][counter]['stats']['kills']['value']
                    }
                    json_object = json.dumps(data_dict, indent=4)
                    with open("data.json", "w") as outfile:
                        outfile.write(json_object)
                counter += 1

            print('updated')
            time.sleep(UPDATE_SLEEP)

        else:
            print(res.status_code)
            exit()



if __name__ == "__main__":
    main()
