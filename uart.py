import serial.tools.list_ports
from Adafruit_IO import MQTTClient

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return "COM5"


if getPort() != "None":
    ser = serial.Serial(port=getPort(), baudrate=115200)
    print(ser)

def processData(client, data):
    print(data)
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    # if splitData[1] == "T":
    #     client.publish('temperature', splitData[2])
    # elif splitData[1] == "H":
    #     client.publish('humidity', splitData[2])
    # elif splitData[1] == "L":
    #     client.publish('light', splitData[2])
    if splitData[1] == "L":
        client.publish('led', splitData[2])
    if splitData[1] == "F":
        client.publish('machine', splitData[2])

mess = ""

def readSerial(client):
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(client, mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]

def writeData(data):
    ser.write(str(data).encode('utf-8'))