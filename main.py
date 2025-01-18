import network
import socket
from machine import Pin
from utime import sleep
import uasyncio as asyncio
#===========================cw=======================
# setup LED
redLED = Pin(16, Pin.OUT)
power_on = Pin(17, Pin.OUT)
power_off = Pin(18, Pin.OUT)
keyPin = Pin(15, Pin.IN, Pin.PULL_UP)  # Assuming the switch is on GPIO 15
keyOffPin = Pin(14, Pin.IN, Pin.PULL_UP)  # Assuming the switch is on GPIO 15

# create needed sleep times for 10 words per minute dot = 0.12 seconds
# 5 words per minute is 0.24 seconds
dot = 0.06
dash = 3 * dot
withinChar = dot
betChar = 3 * dot
betWord = 7 * dot
beacon_delay = 10


def speed(newdot):
    global dot
    global dash
    global withinChar
    global betChar
    global betWord
    global beacon_delay
    dot = newdot
    dash = 3 * dot
    withinChar = dot
    betChar = 3 * dot
    betWord = 7 * dot
   

# make sure LED is off
redLED.off()
power_on.off()
power_off.off()

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

lstmsg = 'test'
serverOn = True
keyOn = False
# function for blinking the LED for a particular letter or number
def charBlinks(char):
    global lstmsg
    global dot
    global serverOn
    # if the character is a space, sleep the between word time
    if char == ' ':
        # assuming that the space is inside the message (not the first character)
        # for a space, we need to sleep "betWord - 3*dot" since the blinking code always sleeps
        # betChar (=3*dot) at the end of each character
        sleep(betWord - 3*dot)
    if char == 'K':
        serverOn = False
        return
    if char == 'P':
        power_on.on()
        sleep(8*dot)
        print("got P")
        power_on.off()
        lstmsg = 'P'
        return
    if char == 'O':
        power_off.on()
        sleep(8*dot)
        print("got O")
        power_off.off()
        lstmsg = 'O'
        return
    if char == 'S':
        speed(dot+0.005)
        lstmsg = 'S'
        print(str(dot))
        return
    if char == 'F':
        speed(dot-0.005)
        lstmsg = 'F'
        return
    elif char == 'D':
        if lstmsg == 'D':
            return
        redLED.on()
        lstmsg = 'D'
        print('D')
        return
    elif char == 'U':
        if lstmsg == 'U':
            return
        redLED.off()
        lstmsg = 'U'
        print('U')
        return
    else:
        lstmsg = 'M'
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
led = machine.Pin('LED', machine.Pin.OUT)

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
    
async def send_sk(cwmsg):
    keylist = cwmsg.split(" ")
    cw = 1
    for pdl in keylist:
        if cw == 1:
            redLED.on()
            if float(pdl) > 2000:
               pdl = "2000" 
            sleep(float(pdl)/1000)
            cw = 0
        else:
            redLED.off()
            if float(pdl) > 2000:
               pdl = "2000" 
            sleep(float(pdl)/1000)
            cw = 1
    redLED.off()



async def monitorKey():
    global serverOn
    print("entered monitorKey")
    while True:
        if keyOffPin.value() == 0:
            print("stopping straight key")
            serverOn = True
            return
        if serverOn == False:
            print("waiting on key")
            if keyPin.value() == 0:  # Assuming LOW when key is pressed (active-low)
                redLED.on()  # Turn on LED when key is pressed
                print("key down")
            else:
                redLED.off()  # Turn off LED when key is released
        await asyncio.sleep(0.01)  # Small delay to debounce and prevent rapid polling

# Listen for connections
async def serverloop():
    global serverOn
    while True:
        print("waiting at top of server loop")
        try:
            if serverOn == True:
                print("waiting for accept")
                cl, addr = s.accept()
                print('client connected from', addr)
                request = cl.recv(2048) 
                print(request)

                request = str(request)
                led_on = request.find('/light/on')
                sk_go = request.find('/light/skgo')
                led_off = request.find('/light/off')

                m_start = request.find('msg')
                m_end = request.find(' HTTP')
    
                msg = ""
                if(m_end != -1):
                    msg = request[m_start+4:m_end]
                    msg = msg.replace("%2F", "/")
                    msg = msg.replace("+", " ")
                    msg = msg.replace("%3F", "?")

                if led_on == 6:
                    #output morse code
                    response = webpage("0", msg)
                    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                    cl.send(response)
                    cl.close()
                    print("sending msg")
                    asyncio.run(send_msg(msg))
                    led.value(1)
                    msg = ""
                elif sk_go == 6:
                    response = webpage("0", msg)
                    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                    cl.send(response)
                    cl.close()
                    asyncio.run(send_sk(msg[:-1]))
                    led.value(1)
                    msg = ""
            else:
                return
        except OSError as e:
            #s.close()
            cl.close()
            print('connection closed ' + str(e))
        print("waiting in server loop")
        #await asyncio.sleep(0.1)  # Small delay to debounce and prevent rapid polling
    
async def main():
    # Create a background task for monitorKey and run it
    while True:
        task_server = asyncio.create_task(serverloop())
        task_mon = asyncio.create_task(monitorKey())

# The main loop for other tasks can go here. 
    # You can add other async tasks that need to run in parallel with monitorKey.
    #while True:
    #    await asyncio.sleep(1)  # Keep the main loop running and allow other tasks to run.
        await task_server
        await task_mon
        await asyncio.sleep(0.1)  # Small delay to debounce and prevent rapid polling






ssid = ''
password = ''





# Just making our internet connection
ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)  
    
while ap.active() == False:
    pass
print('AP Mode Is Active, You can Now Connect')
print('IP Address To Connect to:: ' + ap.ifconfig()[0])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)
asyncio.run(send_msg("c"))

asyncio.run(main())


