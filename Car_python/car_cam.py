## edit on file.txt 1
from picamera import PiCamera
from time import sleep
from sys import exit
camera = PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 32
camera.start_preview()

#count=972
f = open("out.txt", "a+")
def cam(action,count):
    global f
#        sleep(5)
#    for i in range(20):
    camera.capture('%s.jpg' % count)
    f.write('%s.jpg %s\n' % (count,action))
#    count+=1
        

   
def end_cam():
    global f
    f.close()
    camera.stop_preview()
    exit(0)
    

