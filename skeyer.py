import requests
import keyboard
import pygame
import time
import threading
from keyboard._keyboard_event import KEY_DOWN, KEY_UP
from math import trunc
import serial

"""
Since this script has to run as root ('cuz Keyboard), you have to install
the libraries using sudo:
```
sudo pip3 install pyserial
sudo pip3 install keyboard
sudo pip3 install pygame
```
This probably isn't required on Windows.
"""
keydown = 0
dtime = 0
utime = 0
cwmsg = ""
ser_try_again: float = 0.0

# change to your serial port. On windows, this is something like 'COM5'  Set to None to disable serial port stuff.
serial_port: str = "/dev/ttyUSB0"  
ser: serial.Serial = None
prev_cts: bool

# Initialize Pygame
pygame.mixer.init()

# Function to play the sidetone
def play_sidetone():
    pygame.mixer.music.load("sidetone.wav")
    pygame.mixer.music.play(-1)

# Function to stop the sidetone
def stop_sidetone():
    pygame.mixer.music.stop()

# Function to play sidetone while key is pressed
def key_press():
    global keydown
    global dtime
    global utime
    global cwmsg
    print("keydown " + str(keydown))
    if keydown == 0:
        dtime = time.time()
        keydown = 1
        if utime != 0:
            utime = time.time() - utime
            print("full utime " + str(trunc(round(utime*1000,3))))
            cwmsg = cwmsg + str(trunc(round(utime*1000,3)))+"+"
        play_sidetone()

# Function to stop sidetone when key is released
def key_release():
    global keydown
    global dtime
    global utime
    global cwmsg
    keydown = 0
    dtime = time.time() - dtime
    print("full dtime " + str(trunc(round(dtime*1000,3))))
    cwmsg = cwmsg + str(trunc(round(dtime*1000,3)))+"+"
    utime = time.time()
    stop_sidetone()

def esc_pressed():
    global cwmsg
    global dtime
    global utime
    global keydown
    print("found esc")
    print(cwmsg)
    msg_s = requests.get('http://192.168.4.1/light/skgo?msg='+cwmsg)
    cwmsg = ""
    dtime = 0
    utime = 0
    keydown = 0
    print("cleared " + cwmsg)

def on_action(event):
    if event.name == "esc":
        esc_pressed()
    elif event.event_type == KEY_DOWN:
        key_press()
    elif event.event_type == KEY_UP:
        key_release()

# Main function
def main():
    global cwmsg
    global dtime
    global utime
    global keydown

    # Start listening for key events
    # TODO from N6MTS: Look at keyboard.on_press_key and .on_release_key.
    # You can map events directly to callbacks, without needing a 
    # central on_action() director function.
    keyboard.hook(lambda e: on_action(e))

    # Get the serial port immediately upon starting.
    ser_try_again = time.time() - 1.0
    ser = None
    try:
        while True:
            # Moved ESC processing to its own event handler.
            # Serial is polling, so it has to stay in the event loop.
            if serial_port is not None:
                try:
                    if ser is None and time.time() > ser_try_again:
                        # Try opening the serial port
                        ser = serial.Serial(serial_port)
                        prev_cts = ser.cts
                        print("Got serial")
                    cts = ser.cts
                except OSError:   # TODO this could be made more explicit.
                    ser = None
                    print("Couldn't get serial. Trying again in 3 seconds.")
                    ser_try_again = time.time() + 3

                if cts != prev_cts:
                    #print(f"serial key: {cts}")
                    if cts:
                        key_press()
                    else:
                        key_release()
                    prev_cts = cts

            # Don't spin infinitely, just 1000 times a second.
            time.sleep(0.001)


    except KeyboardInterrupt:
        print("Exiting...")
        exit = 1


if __name__ == "__main__":
    main()
  
