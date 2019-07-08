from pynput import keyboard
from sys import exit
from pwm import *
import time
import threading
thread = []
dc=int(0.5*4096)


end=False


    
inA1 = 0 # motor A in1
inA2 = 1 # motor A in2
inB = 2 # motor B  servo
#    motor A
set_pwm(inA1,0)
set_pwm(inA2,0)
inc = 40
right_flag,left_flag=0,0
#motor B(0.9ms-2.1ms) (50Hz-period=>20ms
set_pwm(inB,0)
def position(angel) : 
        x=(angel*1.2/120.0)+0.9
        var=int((x/20)*4096)
##        if speed_dc>0:
##           forward(speed_dc)
        set_pwm(inB,var)
##        time.sleep(0.25)
        print(var)
position(60)
time.sleep(2)
def forward(dc):
    set_pwm(inA1,dc)
    set_pwm(inA2,0)

def backward(dc):
    set_pwm(inA1,0)
    set_pwm(inA2,dc)

def stop():
    set_pwm(inA1,0)
    set_pwm(inA2,0)
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
        if(key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
            position(60)
            forward(dc)
            #set_pwm(inB,307)
        if(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
            backward(dc)
            action="60"
        if(key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):
            global flag
            global inc
            #right_flag=1
            position(120)
        if(key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
            global inc
            #left_flag=1
            position(0) 
        if(key == keyboard.KeyCode(char='h')):
            if(dc!=100):
                dc=(dc+10)%110
            print(dc)
        if(key == keyboard.KeyCode(char='l')):
            if(dc!=0):
                dc=(dc-10)%100
            print(dc)
        if(key == keyboard.KeyCode(char='b')):
##            print ("stop-+6")
##            count_file = open ('count.txt',"w")
##            count_file.write(str(count))
##            count_file.close()
##            print(count)
            end=True
            time.sleep(2)
            stop()
            #GPIO.cleanup()  
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
        
   
    
t2 = threading.Thread(target=listen_key_Thread, args=[])
t3 = threading.Thread(target=servo_Thread, args=[])
t2.start()
t3.start()




