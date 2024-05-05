import sys
from Adafruit_IO import MQTTClient
import time
from uart import *
import requests
import json

URL = ""

AIO_FEED_ID = ["temperature", "humidity", "light", "led", "machine"]
AIO_USERNAME = "Vy2908"
AIO_KEY = ""

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_ID:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload)
    if  feed_id == "led":
        if payload == "0":
            writeData("1")
        else:
            writeData("2")
    if feed_id == "machine":
        if payload == "0":
            writeData("3")
        else:
            writeData("4")      
    

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

def updateData(client, id):
    q = URL + f"?id={id}"

    req = requests.get(q)
    data = json.loads(req.text)[0]

    humi = data["humidity"]
    temp = data["temperature"]
    light = data["light"]

    if temp > 35:
        writeData("4")
        client.publish('machine', 1)
    if temp < 20:
        writeData("3")
        client.publish('machine', 0)
    if light > 6000:
        writeData("1")
        client.publish('led', 0)
    if light < 2000:
        writeData("2")
        client.publish('led', 1)

    client.publish('humidity', humi)
    client.publish('temperature', temp)
    client.publish('light', light)

id = 1
counter = 10
while True:
    readSerial(client)
    if counter == 0:
        counter = 10
        updateData(client, id)
        id = id + 1
    counter = counter - 1
    time.sleep(5)     