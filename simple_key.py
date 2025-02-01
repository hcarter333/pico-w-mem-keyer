import requests
from time import sleep 

try:
    while True:
        print("sending")
        msg_s = requests.get('http://192.168.4.1/light/on?msg=cq+de+kd0fnr+kd0fnr+k')
        print("msg sent")
        sleep(23)

except KeyboardInterrupt:
    print("Exiting...")
    exit = 1
