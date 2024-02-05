import network
import socket
from machine import Pin
from utime import sleep
import uasyncio as asyncio
#===========================cw=======================
# setup LED
redLED = Pin(15, Pin.OUT)
#redLED = Pin('LED', Pin.OUT)

# create needed sleep times for 10 words per minute dot = 0.12 seconds
# 5 words per minute is 0.24 seconds
dot = 0.06
dash = 3 * dot
withinChar = dot
betChar = 3 * dot
betWord = 7 * dot
beacon_delay = 10

# make sure LED is off
redLED.off()

# dictionary for letters and numbers linked to the Morse code for that character
morseCode = {
    'a' : '.-',    'b' : '-...',  'c' : '-.-.',
    'd' : '-..',   'e' : '.',     'f' : '..-.',
    'g' : '--.',   'h' : '....',  'i' : '..',
    'j' : '.---',  'k' : '-.-',   'l' : '.-..',
    'm' : '--',    'n' : '-.',    'o' : '---',
    'p' : '.--.',  'q' : '--.-',  'r' : '.-.',
    's' : '...',   't' : '-',     'u' : '..-',
    'v' : '...-',  'w' : '.--',   'x' : '-..-',
    'y' : '-.--',  'z' : '--..',  '1' : '.----',
    '2' : '..---', '3' : '...--', '4' : '....-',
    '5' : '.....', '6' : '-....', '7' : '--...',
    '8' : '---..', '9' : '----.', '0' : '-----',
    '/' : '-..-.', '?' : '..--..'
    }

# function for blinking the LED for a particular letter or number
def charBlinks(char):
    # if the character is a space, sleep the between word time
    if char == ' ':
        # assuming that the space is inside the message (not the first character)
        # for a space, we need to sleep "betWord - 3*dot" since the blinking code always sleeps
        # betChar (=3*dot) at the end of each character
        sleep(betWord - 3*dot)
    else:
        # look up character in morseCode dictionary - make lowercase if needed
        mCode = morseCode.get(char.lower())
        # if the code is found - blink the code
        if mCode:
            print(char, mCode)
            # need to know number of dot/dashes to do the between character timing
            lenCode = len(mCode)
            # counter to know when we get to the last dot/dash in mCode
            count = 0
            for symbol in mCode:
                # tract place in mCode
                count += 1
                if symbol == '.':
                    # blink a dot
                    redLED.on()
                    sleep(dot)
                    redLED.off()
                    if count == lenCode:
                        # character blinks finished - sleep the between character time
                        sleep(betChar)
                    else:
                        sleep(withinChar)
                if symbol == '-':
                    # blink a dash
                    redLED.on()
                    sleep(dash)
                    redLED.off()
                    if count == lenCode:
                        # character blinks finished - sleep the between character time
                        sleep(betChar)
                    else:
                        sleep(withinChar)
        else:
            # print this if the code for the character is not found
            print('No Morse code for this character:', char)
    



#===========================cw======================


from machine import Pin

led = machine.Pin('LED', machine.Pin.OUT)

#led = Pin(15, Pin.OUT)

html = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title>
    </head>
    <body> <h1>Pico W</h1>
        <p>%s</p>
    </body>
</html>

"""
def webpage(temperature, state):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <link rel="icon" href="data:;base64,iVBORw0KGgo=">
            </head>
            <form action="./on">
            <input type="text" id="msg" name="msg"><br><br>
            <input type="submit" value="Light on" /><br>
            </form>
            <form action="./off">
            <input type="submit" value="Light off" />
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature}</p>
            </body>
            </html>
            """
    return(html)

async def send_msg(msg):
    for char in msg:
        charBlinks(char)
    


ssid = ''
password = ''

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

max_wait = 20

while max_wait > 0:

    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...' + str(max_wait))
    sleep(2)

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
        m_end = request.find(' HTTP')

        print('start ' + str(m_start) + ' end ' + str(m_end))

        msg = ""
        if(m_end != -1):
            msg = request[m_start+4:m_end]
            msg = msg.replace("%2F", "/")
            msg = msg.replace("+", " ")
            msg = msg.replace("%3F", "?")
            print('message ' + msg)
        
        stateis = "Who are you?"

        if led_on == 6:
            #output morse code
            response = webpage("0", msg)
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()
            asyncio.run(send_msg(msg))
            #for char in msg:
            #    charBlinks(char)
            print("led on")
            led.value(1)
            stateis = "Message sent"

        if led_off == 6:
            print("led off")
            led.value(0)
            stateis = "LED is OFF"
        
        #if(request.find('favicon') != -1):
           #cl.send('HTTP/1.0 404 Not FFOUND\r\n\r\nPage Not Found')
           #cl.close
        #response = html % stateis
        #response = webpage("0", msg)
        #cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        #cl.send(response)
        #cl.close()

    except OSError as e:
        s.close()
        cl.close()
        print('connection closed')
