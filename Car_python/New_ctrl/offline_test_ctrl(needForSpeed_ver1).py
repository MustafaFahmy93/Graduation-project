from pynput import keyboard
from sys import exit
flag_up=0
flag_right=0
flag_left=0
def on_press(key):
    global flag_up,flag_right,flag_left
    if((key == keyboard.Key.up or key == keyboard.KeyCode(char='w')) and flag_right==0 and flag_left==0):
        flag_up=1
        print("forward")
    elif(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
        print("backward")
    elif((key == keyboard.Key.right or key == keyboard.KeyCode(char='d'))and flag_up==0):
        flag_right=1
        print("right")
    elif((key == keyboard.Key.left or key == keyboard.KeyCode(char='a'))and flag_up==0):
        flag_left=1
        print("left")
    elif(key == keyboard.KeyCode(char='b')):
        print ("bye bye")
        exit(0)
#================================(up_right & up_left)======================
    if((key == keyboard.Key.right and flag_up==1)or(key == keyboard.Key.up and flag_right==1)):
        print("up right")
    elif((key == keyboard.Key.left and flag_up==1)or(key == keyboard.Key.up and flag_left==1)):
        print("up left")


def on_release(key):
    global flag_up,flag_right,flag_left
    if(key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
        flag_up=0
        print("stop forward")
    elif(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
        print("stop backward")
    elif(key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):      
        flag_right=0
        print("stop right")
    elif(key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
        flag_left=0
        print("stop left")


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
