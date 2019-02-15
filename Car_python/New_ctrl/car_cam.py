import scipy.misc
import cv2
from picamera import PiCamera
from time import sleep
from sys import exit
camera = PiCamera()
camera.resolution = (455, 256)
camera.framerate = 32
camera.start_preview()

f = open("out.txt", "a+")
def cam(action,count):
    global f
    camera.capture('%s.jpg' % count)
    f.write('%s.jpg %s\n' % (count,action))
    full_image = scipy.misc.imread("%s.jpg"% count, mode="RGB")
    cv2.imshow("frame", cv2.cvtColor(full_image, cv2.COLOR_RGB2BGR))

def end_cam():
    global f
    f.close()
    camera.stop_preview()
    exit(0)
    