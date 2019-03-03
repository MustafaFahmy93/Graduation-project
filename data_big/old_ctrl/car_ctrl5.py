#from car_cam import *
from picamera import PiCamera
from pynput import keyboard
from sys import exit
#from gpio_init import *
import RPi.GPIO as GPIO
import time
import threading
#init()
thread = []
dc=70
action="0"  

count = 7
count_file = open ('count.txt',"r")
end=False
'''
def camThread():
    global action,count,end
    camera = PiCamera()
    camera.resolution = (455, 256)
    camera.framerate = 4
    count_file = open("count.txt","r")
    count=int(count_file.read())+1
    print(count)
    imgCount=count
    count_file.close()
    f = open("out.txt", "a+")
    start = time.time()
    while(!end):
        camera.capture('%s.jpg' % count,use_video_port = True)
        f.write('%s.jpg %s\n' % (count,action))
        count+=1
    f.close()
    duration = time.time() - start
    print("Captured: "+ str(count-imgCount))
    print("Duration: " + str(duration))
    '''
inA1 = 15 #12 motor A in1
inA2 = 12 #15 motor A in2
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
flag = 0
inc = 73
#motor B(0.9ms-2.1ms) (50Hz-period=>20ms
GPIO.setmode(GPIO.BOARD)
GPIO.setup(inB,GPIO.OUT)
p3=GPIO.PWM(inB,50)
p3.start(7.5) #(0 degree)
time.sleep(2)
p3.ChangeDutyCycle(7.5)
time.sleep(2)
p3.ChangeDutyCycle(0)
def position(angel,speed_dc) : 
        x=(angel*1.2/120.0)+0.9
        var=(x/20)*100
        if speed_dc>0:
           forward(speed_dc)
        p3.ChangeDutyCycle(var)
#        time.sleep(0.001)
        #p3.ChangeDutyCycle(0)
        #time.sleep(0.25)
        #print(var)
        
        
def forward(dc):
    p1.ChangeDutyCycle(dc)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(7.5)
    
#    time.sleep(0.5)
#    print("f")
def backward(dc):
#    print("b")
    position(73, 0)
    global inc
    inc = 73
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(dc)
    

def stop():
    print("stop")
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(0)#7.5


def listen_key_Thread():
    def on_press(key):
        global dc,t1,thread
        global action
        global count,end
        if(key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
            forward(dc)
            global inc
            inc = 60
            print(inc-60)
    #        print("forward")
            action=inc - 60
#        if(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
#            backward(dc)
#    #        print("backward")
#    #        action="60"
        if(key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):
            global flag
            global inc 
            #flag=1
            if inc<120:
                inc = inc + 5
            #print (flag)
            position(inc, dc)
            print(inc-60)
            action=str(inc-60)
        if(key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
            global inc 
            if inc > 0 :
                inc = inc - 5
            position(inc,dc)
            print(inc-60)
            action=str(inc-60)
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
            count_file = open ('count.txt',"w")
            count_file.write(str(count))
            count_file.close()
            p3.ChangeDutyCycle(7.5)
            time.sleep(2)
            p1.stop()
            p2.stop()
            p3.stop()
            GPIO.cleanup()
            end=True     
            exit(0)

    def on_release(key):
        global flag
        flag = 0
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
        
   
    
#t1 = threading.Thread(target=camThread, args=[])
t2 = threading.Thread(target=listen_key_Thread, args=[])

t2.start()

#t1.start()


