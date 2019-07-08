import RPi.GPIO as GPIO
#def init():
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
#    print("int")
def forward(dc) :
    p1.ChangeDutyCycle(dc)
    p2.ChangeDutyCycle(0)
#    print("f")
def backward(dc):
#    print("b")
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(dc)    
def left(dc):
#    print("l")
    forward(dc)
    GPIO.output(inB1,GPIO.HIGH)
    GPIO.output(inB2,GPIO.LOW)
def right (dc):
#    print("r")
    forward(dc)
    GPIO.output(inB1,GPIO.LOW)
    GPIO.output(inB2,GPIO.HIGH)
def stop():
#    print("s")
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    GPIO.output(inB1,GPIO.LOW)
    GPIO.output(inB2,GPIO.LOW)
def angel90():
#    print("90")
    GPIO.output(inB1,GPIO.LOW)
    GPIO.output(inB2,GPIO.LOW)


