import requests
import json
from Adafruit_IO import MQTTClient

URL = "http://localhost:3000/env"

def updateData(client, id):
    q = URL + f"?id={id}"

    req = requests.get(q)
    data = json.loads(req.text)[0]

    humi = data["humidity"]
    temp = data["temperature"]
    client.publish('humidity', humi)
    client.publish('temperature', temp)

    print(req.text)
    print(humi)
