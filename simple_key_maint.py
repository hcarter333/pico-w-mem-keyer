import requests
from time import sleep 

try:
    while True:
        print("sending")
        msg_s = requests.get('http://192.168.4.1/light/on?msg=cq+de+kd0fnr%2F6+kd0fnr%2F6+kd0fnr%2F6+k')
        print("msg sent")
        sleep(23)
        print("sending")
        msg_s = requests.get('http://192.168.4.1/light/on?msg=cq+de+kd0fnr%2F6+kd0fnr%2F6+kd0fnr%2F6+k')
        print("msg sent")
        sleep(300)

except KeyboardInterrupt:
    print("Exiting...")
    exit = 1
