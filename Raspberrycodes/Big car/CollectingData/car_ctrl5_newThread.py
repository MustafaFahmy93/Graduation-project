#bflrobhhhhhhmb cbam bimport *
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

def camThread():
    global action,count,end
    camera = PiCamera()
    camera.resolution = (455, 256)
    camera.framerate = 32
    count_file = open("count.txt","r")
    count=int(count_file.read())+1
    print(count)
    imgCount=count
    count_file.close()
    f = open("out.txt", "a+")
    start = time.time()
    while(not end):
        camera.capture('%s.jpg' % count,use_video_port = False)
        f.write('%s.jpg %s\n' % (count,action))
        count+=1
    f.close()
    duration = time.time() - start
    print("Captured: "+ str(count-imgCount))
    print("Duration: " + str(duration))
    
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
inc = 40
#motor B(0.9ms-2.1ms) (50Hz-period=>20ms
GPIO.setmode(GPIO.BOARD)
GPIO.setup(inB,GPIO.OUT)
p3=GPIO.PWM(inB,50)
p3.start(6.5) #(0 degree)
time.sleep(2)
p3.ChangeDutyCycle(6.5)
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
#    p3.ChangeDutyCycle(7.5)
    
#    time.sleep(0.5)
#    print("f")
def backward(dc):
#    print("b")
    position(40, -2)
    global inc
    inc = 40
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(dc)
    

def stop():
    print("stop")
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    p3.ChangeDutyCycle(0)#7.5
right_flag=0
left_flag=0
def servo_Thread():
    global end,right_flag,left_flag,inc,action,dc
    while(not end):
        if(right_flag==1):
            if inc<80:
                inc = inc + 5
            #print (flag)
            position(inc, dc)
#            print(inc-40)
            action=str(inc-40)
        elif(left_flag==1):
            if inc > 0 :
                inc = inc - 5
            position(inc,dc)
#            print(inc-40)
            action=str(inc-40)
        time.sleep(0.1)
def listen_key_Thread():
    def on_press(key):
        global dc,t1,thread
        global action
        global count,end,right_flag,left_flag
        if(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
            print("backward")
            
            #backward(dc)
            

            
        if(key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
#            forward(dc)
            position( 40 ,dc)
            global inc
            inc = 40
#            print(inc-40)
    #        print("forward")
            action=inc - 40
#        if(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
#            backward(dc)
#    #        print("backward")
#    #        action="60"
        if(key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):
            global flag
            global inc
            right_flag=1
            #flag=1
#            if inc<120:
#                inc = inc + 5
#            #print (flag)
#            position(inc, dc)
#            print(inc-60)
#            action=str(inc-60)

        if(key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
            global inc
            left_flag=1 
#            if inc > 0 :
#                inc = inc - 5
#            position(inc,dc)
#            print(inc-60)
#            action=str(inc-60)
        if(key == keyboard.KeyCode(char='h')):
            if(dc!=100):
                dc=(dc+10)%110
            print(dc)
        if(key == keyboard.KeyCode(char='l')):
            if(dc!=0):
                dc=(dc-10)%100
            print(dc)
        if(key == keyboard.KeyCode(char='b')):
            print ("stop-+6")
            count_file = open ('count.txt',"w")
            count_file.write(str(count))
            count_file.close()
            print(count)
            p3.ChangeDutyCycle(6.5)
            end=True
            time.sleep(2)
            p1.stop()
            p2.stop()
            p3.stop()
            GPIO.cleanup()
            #end=True     
            exit(0)

    def on_release(key):
        global flag,right_flag,left_flag
        flag = 0
        if(key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
#            print("up stop")
            stop()
        elif(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
#            print("down stop")
            stop()
        elif(key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):
#            print("r stop")
            right_flag=0
            stop() 
        elif(key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
#            print("l stop")
            left_flag=0
            stop()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:      
        listener.join()
        
   
    
t1 = threading.Thread(target=camThread, args=[])
t2 = threading.Thread(target=listen_key_Thread, args=[])
t3 = threading.Thread(target=servo_Thread, args=[])
t2.start()
t3.start()
t1.start()


