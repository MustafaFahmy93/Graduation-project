from car_cam import *
from pynput import keyboard
from sys import exit
from gpio_init import *
select_car_init("small")
import threading
thread = []
dc=47
action="1 0 0 0"  
flag_up=0
flag_right=0
flag_left=0
count=-1
def camThread():
    global action,count
    count_file = open("count.txt","r")
    count=count_file.read()
    count_file.close()
    for i in range(10000):
        cam(action,count)
        print(count)
        count+=1
        if(action=="end"):
            end_cam()
            t1.do_run = False
            break
def listen_key_Thread():
    def on_press(key):
        global flag_up,flag_right,flag_left
        global dc,action,count
        if((key == keyboard.Key.up or key == keyboard.KeyCode(char='w')) and flag_right==0 and flag_left==0):
            flag_up=1
            dc=50
            forward(dc)
            action="1 0 0 0"
        elif(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
            dc=50
            backward(dc)
            action="0 0 0 1"
        elif((key == keyboard.Key.right or key == keyboard.KeyCode(char='d'))and flag_up==0):
            flag_right=1
            dc=50
            right(dc)
            action="0 1 0 0"
        elif((key == keyboard.Key.left or key == keyboard.KeyCode(char='a'))and flag_up==0):
            flag_left=1
            dc=50
            left(dc)
            action="0 0 1 0"
        elif(key == keyboard.KeyCode(char='h')):
            if(dc!=100):
                dc=(dc+10)%110
            print(dc)
        elif(key == keyboard.KeyCode(char='l')):
            if(dc!=0):
                dc=(dc-10)%100
            print(dc)
        elif(key == keyboard.KeyCode(char='b')):
            count_file = open("count.txt","w")
            count_file.write(str(count))
            print(count)
            count_file.close()
            action="end"
            stop_FB()
            stop_RL()
            end_GPIO()
            exit(0)
#================================(up_right & up_left)======================
        if(key == keyboard.Key.right and flag_up==1):
            dc=60
            forward(dc)
            right(dc)
            action="0 1 0 0"
        elif(key == keyboard.Key.left and flag_up==1):
            dc=60
            forward(dc)
            left(dc)
            action="0 0 1 0"
        elif(key == keyboard.Key.up and flag_right==1):
            dc=60
            forward(dc)
            right(dc)
            action="0 1 0 0"
        elif(key == keyboard.Key.up and flag_left==1):
            dc=60
            forward(dc)
            left(dc)
            action="0 0 1 0"



    def on_release(key):
        global flag_up,flag_right,flag_left
        if(key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
            flag_up=0
            stop_FB()
        elif(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
            stop_FB()
        elif(key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):      
            flag_right=0
            stop_RL()
        elif(key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
            flag_left=0
            stop_RL()


    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


t1 = threading.Thread(target=camThread, args=[])
t2 = threading.Thread(target=listen_key_Thread, args=[])

t2.start()
t1.start()
