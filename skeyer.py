import requests
import keyboard
import pygame
import time
import threading
from keyboard._keyboard_event import KEY_DOWN, KEY_UP
from math import trunc
keydown = 0
dtime = 0
utime = 0
cwmsg = ""
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

def on_action(event):
    if event.name != "esc":
        if event.event_type == KEY_DOWN:
            key_press()

        elif event.event_type == KEY_UP:
            key_release()
    else:
        print("found esc")

# Main function
def main():
    global cwmsg
    global dtime
    global utime
    global keydown
    # Start listening for key events
    keyboard.hook(lambda e: on_action(e))

    try:
        while True:
            # Block the main thread
            keyboard.wait("esc")  # Wait until the "esc" key is pressed
            print(cwmsg)
            msg_s = requests.get('http://192.168.4.1/light/skgo?msg='+cwmsg)
            cwmsg = ""
            dtime = 0
            utime = 0
            keydown = 0
            print("cleared " + cwmsg)


    except KeyboardInterrupt:
        print("Exiting...")
        exit = 1


if __name__ == "__main__":
    main()
  
