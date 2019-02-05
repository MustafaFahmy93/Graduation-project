## edit on file.txt 1
#from car_cam import *
from pynput import keyboard
from sys import exit
#from gpio_init import *
import RPi.GPIO as GPIO
import time
import threading
#init()
thread = []
dc=100
action="60"  
#def camThread():
#    global action
#    count= 2765
#    for i in range(5000):
#        cam(action,count)
#        print(count)
#        count+=1
#        if(action=="end"):
#            end_cam()
#            t1.do_run = False
#            break
inA1 = 12 #12 motor A in1
inA2 = 15 #15 motor A in2

inB = 16 #16 motor B  servo
#    motor A
GPIO.setmode(GPIO.BOARD)
GPIO.setup(inA1,GPIO.OUT)
p1=GPIO.PWM(inA1,100)
p1.start(0)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(inA2,GPIO.OUT)
p2=GPIO.PWM(inA2,100)
p2.start(0)

#motor B(0.9ms-2.1ms) (50Hz-period=>20ms
GPIO.setmode(GPIO.BOARD)
GPIO.setup(inB,GPIO.OUT)
p3=GPIO.PWM(inB,50)
p3.start(7.5) #(0 degree)
p3.ChangeDutyCycle(7.5)
time.sleep(1)
p3.ChangeDutyCycle(0)
def position(angel,speed_dc) : 
        x=(angel*1.2/120.0)+0.9
        var=(x/20)*100
        #if speed_dc>0:
         #   forward(speed_dc)
        p3.ChangeDutyCycle(var)
        time.sleep(1)
        p3.ChangeDutyCycle(0)
        time.sleep(0.5)
        print(var)
        
        
def forward(dc):
    p1.ChangeDutyCycle(dc)
    p2.ChangeDutyCycle(0)
#    print("f")
def backward(dc):
#    print("b")
    position(60, 0)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(dc)    

#def listen_key_Thread():
def on_press(key):
    global dc,t1,thread
    global action
    if(key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
        position(60,dc)
        print("forward")
        action="60"
    if(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
        backward(dc)
        print("backward")
        action="60"
    if(key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):
        position(120,dc)
        print("right")
        action="120"
    if(key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
        position(0,dc)
        print("left")
        action="0"
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
        position(60,dc)
        p1.stop()
        p2.stop()
        p3.stop()
        GPIO.cleanup()
        action="end"      
        exit(0)

def on_release(key):
    if(key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
        print("up stop")
#            stop()
    elif(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
        print("down stop")
#            stop()
    elif(key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):
        print("r stop")
#        p3.stop()
#            stop()    
    elif(key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
        print("l stop")
#        p3.stop()
#            stop()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:      
    listener.join()
    
   
    
#t1 = threading.Thread(target=camThread, args=[])
#t2 = threading.Thread(target=listen_key_Thread, args=[])
#
#t2.start()
#t1.start()


