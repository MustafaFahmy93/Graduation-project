import RPi.GPIO as GPIO
import time
def init():
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
    time.sleep(.5)
def postion(angel,speed_dc) : 
        x=(angel*1.2/120.0)+0.9
        var=(x/20)*100
#        forward(speed_dc)
        p3.ChangeDutyCycle(angel)
        time.sleep(0.5)
        print(angel)
def forward(dc):
    p1.ChangeDutyCycle(dc)
    p2.ChangeDutyCycle(0)
#    print("f")
def backward(dc):
#    print("b")
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(dc)    


def stop():
    print()
#    p1.ChangeDutyCycle(0)
#    p2.ChangeDutyCycle(0)
#    p3.ChangeDutyCycle(0)#7.5


def end():
    p1.stop()
    p2.stop()
    p3.stop()
    GPIO.cleanup()

