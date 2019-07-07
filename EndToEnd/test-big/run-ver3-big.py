#import tensorflow as tf
import keras 
import scipy.misc
#import model
import cv2
#import stop
import numpy as np
from subprocess import call
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from sys import exit
from gpio_init import *
import keras.backend as K
from keras.models import *
from keras.callbacks import *
import tensorflow as tf 
select_car_init("big")
camera = PiCamera()
camera.resolution = (455, 256)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(455, 256))
#camera.start_preview()
# allow the camera to warmup
time.sleep(0.1)
#camera.capture('image.jpg')
def atan_layer (x) :
    return tf.multiply(tf.atan(x),2)

def atan_layer_shape(input_shape):
    return input_shape

def soft_acc (y_true , y_pred) :
    return K.mean(K.equal(K.round(y_true),K.round(y_pred)))
#sess = tf.InteractiveSession()
#saver = tf.train.Saver()model_retrained_acc_89model_retrained_acc_89model_retrained_acc_89model_retrained_acc_89
#saver.restore(sess, "save/model.ckpt")
model=load_model('model_credit_ta7t.h5',compile=True , custom_objects={'tf':tf,'atan_layer':atan_layer,'atan_layer_shape':atan_layer_shape,'soft_acc':soft_acc})
#dc=50
outAction = open('outAction.txt','a+')
#while(cv2.waitKey(10) != ord('q')):
count=0
start=time.clock()
for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
    
    image_cap = frame.array
    cv2.imwrite("image.jpg",image_cap)
    dummy=cv2.imread("image.jpg")
    
    # openCV code
    full_image = scipy.misc.imread("image.jpg", mode="RGB")
    count+=1
    image = scipy.misc.imresize(full_image[-150:], [66, 200]) / 255.0
    
#    if(stop.stop_condition(dummy)):
#        stopF()
#        stopRL()
##        time.sleep(5)
#        rawCapture.truncate(0)
#        continue
    
    image=np.expand_dims(image, axis=0)
    t1=time.clock()
#    awad=tf.argmax(tf.nn.softmax( model.y),dimension=1).eval(feed_dict={model.x: [image], model.keep_prob: 1.0})
   
    #awad=np.argmax(model.predict(image,batch_size=1))
    awad=model.predict(image,batch_size=1)
    t2=time.clock()
    print("img"+str(count)+": "+str(t2-t1))
    print(awad)
#    degrees=(str(np.squeeze(awad))).strip('[')
#    degrees=degrees.strip(']')
#    print(degrees)
#    outAction.write(degrees +'\n')
#    call("clear")
    cv2.imshow("frame", cv2.cvtColor(full_image, cv2.COLOR_RGB2BGR))
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    degrees+=40
    forward(50)
    position(degrees)
#    delta
#    time.sleep(0.7)
#    stopF()
#    stopRL()
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

end=time.clock()
print("Total: " + str(count))
print("Duration: " + str(end-start))
#    camera.capture('image.jpg')
#    full_image = scipy.misc.imread("image.jpg", mode="RGB")
#    image = scipy.misc.imresize(full_image[-150:], [66, 200]) / 255.0
#    t=time.clock()
#    awad=tf.argmax(tf.nn.softmax( model.y),dimension=1).eval(feed_dict={model.x: [image], model.keep_prob: 1.0})
#    print(awad)
#    t2=time.clock()
#    print(t2-t)
#    degrees=(str(np.squeeze(awad))).strip('[')
#    degrees=degrees.strip(']')
#    print(degrees)
#    outAction.write(degrees +'\n')
#    call("clear")
#    cv2.imshow("frame", cv2.cvtColor(full_image, cv2.COLOR_RGB2BGR))
#    
#    
outAction.close()
stopF()
stopRL()
action="end"

cv2.destroyAllWindows()
