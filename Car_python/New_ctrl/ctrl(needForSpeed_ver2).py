from car_cam import *
from pynput import keyboard
from sys import exit
from gpio_init import *
select_car_init("big")
import threading
thread = []
dc=40
action="0"  
flag_up=0
flag_right=0
flag_left=0
count=-1
inc = 60
def inc_right():
    global inc
    if inc<120:
        inc = inc + 5
    position(inc)
def inc_left():
    global inc 
    if inc > 0:
        inc = inc - 5
    position(inc)
#================================cam====================
def camThread():
    global action,count
    count_file = open("count.txt","r")
    count=count_file.read()
    count_file.close()
    for i in range(10000):
        cam(action,count)
        count+=1
        if(action=="end"):
            end_cam()
            t1.do_run = False
            break
def listen_key_Thread():
#============================on_press=============================
    def on_press(key):
        global flag_up,flag_right,flag_left
        global dc,action,count,inc
        print(action)
        if((key == keyboard.Key.up or key == keyboard.KeyCode(char='w')) and flag_right==0 and flag_left==0):
            flag_up=1
            forward(dc)
            inc=60
            position(60)
            action="0"
        elif(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
            backward(dc)
            inc=60
            position(60)
            action="0"
        elif((key == keyboard.Key.right or key == keyboard.KeyCode(char='d'))and flag_up==0):
            flag_right=1
            inc_right()
            action=(str(inc-60))
        elif((key == keyboard.Key.left or key == keyboard.KeyCode(char='a'))and flag_up==0):
            flag_left=1
            inc_left()
            action=(str(inc-60))
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
            end_GPIO()
            exit(0)
        #================================(up_right & up_left)======================
        if((key == keyboard.Key.right and flag_up==1)or(key == keyboard.Key.up and flag_right==1)):
            forward(dc)
            inc_right()
            action=(str(inc-60))
        elif((key == keyboard.Key.left and flag_up==1)or(key == keyboard.Key.up and flag_left==1)):
            forward(dc)
            inc_left()
            action=(str(inc-60))
#============================on_release=============================
    def on_release(key):
        global flag_up,flag_right,flag_left
        if(key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
            flag_up=0
            stop_FB()
        elif(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
            stop_FB()
        elif(key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):      
            flag_right=0
        elif(key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
            flag_left=0
            


    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


t1 = threading.Thread(target=camThread, args=[])
t2 = threading.Thread(target=listen_key_Thread, args=[])

t2.start()
t1.start()

