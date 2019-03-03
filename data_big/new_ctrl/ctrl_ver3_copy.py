#from car_cam import *
from picamera import PiCamera
from pynput import keyboard
from pynput.keyboard import Key, Controller
keyboard1 = Controller()
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
step=5
#================================cam====================
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
    while(not end):
#        print(action)
        camera.capture('%s.jpg' % count,use_video_port = True)
        f.write('%s.jpg %s\n' % (count,action))
        count+=1
    f.close()
    duration = time.time() - start
    print("Captured: "+ str(count-imgCount))
    print("Duration: " + str(duration))
    '''
def listen_key_Thread():
#============================on_press=============================
    def on_press(key):
        global flag_up,flag_right,flag_left
        global dc,action,count,inc,end
        if((key == keyboard.Key.up or key == keyboard.KeyCode(char='w')) and flag_right==0 and flag_left==0):
            flag_up=1
            forward(dc)
            if(inc>60 and inc != 60):
                inc=inc-step
                if(inc<60):
                    inc=60
            elif(inc<60 and inc != 60):
                inc=inc+step
                if(inc>60):
                    inc=60
            position(inc)
            action=str(inc-60)
#            print("f"+ action)
###            forward(dc)
#            inc=60
###            position(60)
#            action="0"
#        elif(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
#            backward(dc)
#            inc=60
#            position(60)
#            action("0")
        elif((key == keyboard.Key.right or key == keyboard.KeyCode(char='d'))and flag_up==0):
            flag_right=1
#            if inc<120:
#                inc=+step
#                if(inc>120):
#                    inc=120
#            position(inc)
#            action=str(inc-60)
        elif((key == keyboard.Key.left or key == keyboard.KeyCode(char='a'))and flag_up==0):
            flag_left=1
#            if inc > 0:
#                inc=-step
#                if(inc<0):
#                    inc=0
#            position(inc)
#            action=str(inc-60)
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
            end=True
            stop_FB()
            end_GPIO()
            exit(0)
        #================================(up_right & up_left)======================
        if((key == keyboard.Key.right and flag_up==1)or(key == keyboard.Key.up and flag_right==1)):
            forward(dc)
            if inc<120:
                inc=inc+step
                if(inc>120):
                    inc=120
            position(inc)
            action=str(inc-60)
        elif((key == keyboard.Key.left and flag_up==1)or(key == keyboard.Key.up and flag_left==1)):
            forward(dc)
            if inc > 0:
                inc=inc-step
                if(inc<0):
                    inc=0
            position(inc)
            action=str(inc-60)
#============================on_release=============================
    def on_release(key):
        global flag_up,flag_right,flag_left
        if(key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
            flag_up=0
            stop_FB()
#        elif(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
#            stop_FB()
        elif(key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):      
            flag_right=0
            if(flag_up==1): 
                keyboard1.press(Key.up)
        elif(key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
            flag_left=0
            if(flag_up==1): 
                keyboard1.press(Key.up)
            


    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


#t1 = threading.Thread(target=camThread, args=[])
t2 = threading.Thread(target=listen_key_Thread, args=[])

t2.start()
#t1.start()


