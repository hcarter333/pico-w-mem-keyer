import network

import socket

import time




from machine import Pin

led = machine.Pin('LED', machine.Pin.OUT)

#led = Pin(15, Pin.OUT)




ssid = ''

password = ''




wlan = network.WLAN(network.STA_IF)

wlan.active(True)

wlan.connect(ssid, password)




html = """<!DOCTYPE html>

<html>

    <head> <title>Pico W</title> </head>

    <body> <h1>Pico W</h1>

        <p>%s</p>

    </body>

</html>

"""




max_wait = 20

while max_wait > 0:

    if wlan.status() < 0 or wlan.status() >= 3:

        break

    max_wait -= 1

    print('waiting for connection...')

    time.sleep(1)




if wlan.status() != 3:

    raise RuntimeError('network connection failed ' + str(wlan.status()))

else:

    print('connected')

    status = wlan.ifconfig()

    print( 'ip = ' + status[0] )




addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]







s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(addr)

s.listen(1)




print('listening on', addr)




# Listen for connections

while True:

    try:

        cl, addr = s.accept()

        print('client connected from', addr)

        request = cl.recv(1024)

        print(request)




        request = str(request)

        led_on = request.find('/light/on')

        led_off = request.find('/light/off')

        print( 'led on = ' + str(led_on))
        print( 'led off = ' + str(led_off))
        print(' ========================')
        print( 'request = ' + request)
        print(' ========================')

        m_start = request.find('msg')
        m_end = request.find('bk')

        print('start ' + str(m_start) + ' end ' + str(m_end))

        msg = request[m_start+3:m_end]
        print('message ' + msg)
        stateis = "Who are you?"

        if led_on == 6:

            print("led on")
            led.value(1)
            stateis = "LED is ON"

        if led_off == 6:
            print("led off")
            led.value(0)
            stateis = "LED is OFF"

        response = html % stateis

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')

        cl.send(response)

        cl.close()

except OSError as e:
        s.close()
        cl.close()
        print('connection closed')
