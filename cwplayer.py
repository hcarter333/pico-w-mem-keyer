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
pygame.mixer.init()

def play_sidetone():
    pygame.mixer.music.load("sidetone.wav")
    pygame.mixer.music.play(-1)

# Function to stop the sidetone
def stop_sidetone():
    pygame.mixer.music.stop()



cwmsg = "286+150+146+131+254+120+160+233+239+158+304+150+102+114+305+"
keylist = cwmsg.split("+")
cw = 1
for pdl in keylist:
    if cw == 1:
        play_sidetone()
        time.sleep(float(pdl)/1000)
        cw = 0
    else:
        stop_sidetone()
        time.sleep(float(pdl)/1000)
        cw = 1

