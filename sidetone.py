import keyboard
import pygame
import time
import threading
from keyboard._keyboard_event import KEY_DOWN, KEY_UP
keydown = 0
dtime = 0
utime = 0
# Initialize Pygame
pygame.mixer.init()

# Function to play the sidetone
def play_sidetone():
    pygame.mixer.music.load("sidetone.wav")  # Replace "sidetone.wav" with your own sound file
    pygame.mixer.music.play(-1)

# Function to stop the sidetone
def stop_sidetone():
    pygame.mixer.music.stop()

# Function to play sidetone while key is pressed
def key_press():
    global keydown
    global dtime
    global utime
    if keydown == 0:
        dtime = time.time()
        #print("key down")
        #print("start dtime " + str(dtime))
        keydown = 1
        if utime != 0:
            utime = time.time() - utime
            print("full utime " + str(round(utime*1000,3)))
        play_sidetone()

# Function to stop sidetone when key is released
def key_release():
    global keydown
    global dtime
    global utime
    keydown = 0
    #print("key up")
    dtime = time.time() - dtime
    print("full dtime " + str(round(dtime*1000,3)))
    utime = time.time()
    #print("start utime " + str(utime))
    stop_sidetone()

# Callback function for key press event
def on_press(event):
    if event.event_type == keyboard.KEY_DOWN:
        print("key down")
        play_sidetone()

# Callback function for key release event
def on_release(event):
    if event.event_type == keyboard.KEY_UP:
        print("key up")
        stop_sidetone()

def on_action(event):
    if event.event_type == KEY_DOWN:
        key_press()

    elif event.event_type == KEY_UP:
        key_release()

# Main function
def main():
    # Start threads for key press and release events
#    press_thread = threading.Thread(target=key_press)
#    release_thread = threading.Thread(target=key_release)
#
#    press_thread.start()
#    release_thread.start()
#
#    # Wait for threads to finish
#    press_thread.join()
#    release_thread.join()
   
    # Start listening for key events
    keyboard.hook(lambda e: on_action(e))
    #keyboard.on_press(on_key_press)
    #keyboard.on_release(on_key_release)

    # Block the main thread
    keyboard.wait("esc")  # Wait until the "esc" key is pressed

if __name__ == "__main__":
    main()
