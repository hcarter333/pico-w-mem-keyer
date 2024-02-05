import requests
from time import sleep 

try:
    while True:
        myMessage = input('Enter Your Message (a-z, 0-9): ')
        myMessage = myMessage.replace("?", "%3F")
        myMessage = myMessage.replace("/", "%2F")
        myMessage = myMessage.replace(" ", "+")
        msg_s = requests.get('http://10.0.0.170/light/on?msg='+myMessage)
        print("msg sent " + myMessage)

except KeyboardInterrupt:
    print("Exiting...")
    exit = 1
