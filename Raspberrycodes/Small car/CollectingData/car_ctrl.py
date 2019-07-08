## edit on file.txt 1
from car_cam import *
from pynput import keyboard
from sys import exit
from gpio_init import *
import threading
#init()
thread = []
dc=47
action="1 0 0 0"  
def camThread():
    global action
    count= 5000
    for i in range(5000):
        cam(action,count)
        print(count)
        count+=1
        if(action=="end"):
            end_cam()
            
            
            t1.do_run = False
            break
        
def listen_key_Thread():
    def on_press(key):
        global dc,t1,thread
        global action
        if(key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
            dc=50
            forward(dc)
            print("forward")
            action="1 0 0 0"
        if(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
            dc=50
            backward(dc)
            print("backward")
            action="0 0 0 1"
        if(key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):
            dc=60
            forward(dc)
            right(dc)
            print("right")
            action="0 1 0 0"
        if(key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
            dc=60
            forward(dc)
            left(dc)
            print("left")
            action="0 0 1 0"
        if(key == keyboard.KeyCode(char='h')):
            if(dc!=100):
                dc=(dc+10)%110
            print(dc)
        if(key == keyboard.KeyCode(char='l')):
            if(dc!=0):
                dc=(dc-10)%100
            print(dc)
        if(key == keyboard.KeyCode(char='b')):
            print ("stop")
            GPIO.cleanup()
            action="end"
            
            exit(0)
    
    def on_release(key):
        if(key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
            print("up stop")
            stop()
        elif(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
            print("down stop")
            stop()
        elif(key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):
            print("r stop")
            stop()    
        elif(key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
            print("l stop")
            stop()
    
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:      
        listener.join()
        
       
    
t1 = threading.Thread(target=camThread, args=[])
t2 = threading.Thread(target=listen_key_Thread, args=[])

t2.start()
t1.start()


