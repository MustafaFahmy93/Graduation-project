import RPi.GPIO as GPIO
import time 
def select_car_init(sel):
    global inB1,inB2,p1,p2,p3
    if(sel=="big"):#==============================big==========================
        print("big")
        inA1 = 12 #12 motor A in1
        inA2 = 15 #15 motor A in2
        inB  = 16 #16 motor B  servo
        #    motor A
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(inA1,GPIO.OUT)
        p1=GPIO.PWM(inA1,100)
        p1.start(0)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(inA2,GPIO.OUT)
        p2=GPIO.PWM(inA2,100)
        p2.start(0)
        #motor B (0.9ms-2.1ms) (50Hz-period=>20ms)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(inB,GPIO.OUT)
        p3=GPIO.PWM(inB,50)
        p3.start(7.5) #(0 degree)
#        p3.ChangeDutyCycle(7.5)
        time.sleep(0.5)
    elif(sel=="small"):#==============================small==========================
        inA1 = 12 # motor A in1
        inB1 = 15 # motor A in2
        inA2 = 16 # motor B in1
        inB2 = 18 # motor B in2
        #    motor A
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(inA1,GPIO.OUT)
        p1=GPIO.PWM(inA1,100)
        p1.start(0)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(inA2,GPIO.OUT)
        p2=GPIO.PWM(inA2,100)
        p2.start(0)

        #    motor B
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(inB1,GPIO.OUT)
        GPIO.output(inB1,GPIO.LOW)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(inB2,GPIO.OUT)
        GPIO.output(inB2,GPIO.LOW)
#======================Functions====================
def forward(dc):
    global p1,p2
    p1.ChangeDutyCycle(dc)
    p2.ChangeDutyCycle(0)
def backward(dc):
    global p2,p3
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(dc)
def stop_FB():#forward/backward
    global p2,p3
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
def end_GPIO():
    GPIO.cleanup()
#======================Functions(big)====================
def position(angle) :
    global p3
    x=(angle*1.2/120.0)+0.9
    var=(x/20)*100
    p3.ChangeDutyCycle(var)
#    time.sleep(0.001)
#======================Functions(small)====================
def left(dc):
    global inB1,inB2
    GPIO.output(inB1,GPIO.HIGH)
    GPIO.output(inB2,GPIO.LOW)
def right (dc):
    global inB1,inB2
    GPIO.output(inB1,GPIO.LOW)
    GPIO.output(inB2,GPIO.HIGH)
def stop_RL():#right/left
    global inB1,inB2
    GPIO.output(inB1,GPIO.LOW)
    GPIO.output(inB2,GPIO.LOW)

