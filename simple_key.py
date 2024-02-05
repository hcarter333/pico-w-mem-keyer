import requests
from time import sleep 

try:
    while True:
        msg_s = requests.get('http://10.0.0.170/light/on?msg=cq+cq+de+kd0fnr%2F6+kd0fnr%2F6+kd0fnr%2F6+k')
        print("msg sent")
        sleep(43)

except KeyboardInterrupt:
    print("Exiting...")
    exit = 1
