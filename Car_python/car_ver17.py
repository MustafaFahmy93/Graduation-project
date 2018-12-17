from pynput import keyboard
from sys import exit
import RPi.GPIO as GPIO
import time

inA1 = 12 # motor A in1
inA2 = 16 # motor A in2
inB1 = 38 # motor B in1
inB2 = 40 # motor B in2
en1 = 35  # enable 1
en2 = 37  # enable 2

#motor A
    
GPIO.setmode(GPIO.BOARD)
GPIO.setup(inA1,GPIO.OUT)
p1=GPIO.PWM(inA1,100)
p1.start(0)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(inA2,GPIO.OUT)
p2=GPIO.PWM(inA2,100)
p2.start(0)

#motor B

GPIO.setmode(GPIO.BOARD)
GPIO.setup(inB1,GPIO.OUT)
GPIO.output(inB1,GPIO.LOW)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(inB2,GPIO.OUT)
GPIO.output(inB2,GPIO.LOW)

#enable 1
GPIO.setmode(GPIO.BOARD)
GPIO.setup(en1,GPIO.OUT)
GPIO.output(en1,GPIO.HIGH)
#enable 2
GPIO.setmode(GPIO.BOARD)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(en2,GPIO.HIGH)

def forward(dc) :
    p1.ChangeDutyCycle(dc)
    p2.ChangeDutyCycle(0)
def backward(dc):
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(dc)    
def right(dc):
    #forward(dc)
    GPIO.output(inB1,GPIO.HIGH)
    GPIO.output(inB2,GPIO.LOW)
def left (dc):
    #forward(dc)
    GPIO.output(inB1,GPIO.LOW)
    GPIO.output(inB2,GPIO.HIGH)
def stop():
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    GPIO.output(inB1,GPIO.LOW)
    GPIO.output(inB2,GPIO.LOW)
def angel90():
    GPIO.output(inB1,GPIO.LOW)
    GPIO.output(inB2,GPIO.LOW)


dc=0
text_file = open("Output.txt", "w")


def on_press(key):
    global dc
    #text_file.write("action: %c \n" % dir)
    if(key == keyboard.KeyCode(char='h')):
        if(dc!=100):
            dc=(dc+10)%110
        print(dc)
    if(key == keyboard.KeyCode(char='l')):
        if(dc!=0):
            dc=(dc-10)%100
        print(dc)
    
    if(key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
        forward(dc)
        text_file.write("forward \n")
        print("forward")
    if(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
        backward(dc)
        text_file.write("backward \n")
        print("backward")
    if(key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):
        forward(dc)
        right(dc)
        text_file.write("right \n")
        print("right")
    if(key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
        forward(dc)
        left(dc)
        text_file.write("right \n")
        print("left")
    if(key == keyboard.KeyCode(char='b')):
        print ("stop")
        GPIO.cleanup()
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