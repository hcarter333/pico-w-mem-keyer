import requests
from time import sleep 
import datetime

try:
    while True:
        myMessage = input('Enter Your Message (a-z, 0-9): ')
        myMessage = myMessage.replace("?", "%3F")
        myMessage = myMessage.replace("/", "%2F")
        myMessage = myMessage.replace(" ", "+")
        msg_s = requests.get('http://192.168.4.1/light/on?msg='+myMessage)
        print("msg sent " + myMessage)
        print(str(datetime.datetime.now()))
except KeyboardInterrupt:
    print("Exiting...")
    exit = 1
