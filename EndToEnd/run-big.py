#in order to force keras to run on CPU
import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]=""
#import tensrflow as tf
import keras 
import scipy.misc
#import model
import cv2
import stop
import numpy as np
from subprocess import call
import time
cap = cv2.VideoCapture("/dev/video1")
cap.set(cv2.CAP_PROP_FRAME_WIDTH,455)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,256)

from scipy import pi
from sys import exit
from ctrl import *
import keras.backend as K
from keras.models import *
from keras.callbacks import *
from keras.models import Sequential
from keras.layers import Activation,Dropout,Lambda
from keras.layers.core import Dense,Flatten
from keras.optimizers import Adam
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import *
from keras.initializers import TruncatedNormal,Constant
from keras.regularizers import l2
import tensorflow as tf
#camera = cv2.VideoCapture("/dev/video1")
#camera.resolution = (455, 256)
#camera.framerate = 15
#rawCapture = PiRGBArray(camera, size=(455, 256))
#camera.start_preview()
# allow the camera to warmup
time.sleep(0.1)
#camera.capture('image.jpg')

def getmodel():
    model=Sequential()
    model.add(Conv2D(24,(5,5),strides=(2,2),kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),activation='relu',input_shape=(66,200,3),use_bias=True))
    model.add(Conv2D(36,(5,5),strides=(2,2),kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),activation='relu',input_shape=(31,98,24),use_bias=True))
    model.add(Conv2D(48,(5,5),strides=(2,2),kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),activation='relu',input_shape=(14,47,36),use_bias=True))
    model.add(Conv2D(64,(3,3),strides=(1,1),kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),activation='relu',input_shape=(5,22,48),use_bias=True))
    model.add(Conv2D(64,(3,3),strides=(1,1),kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),activation='relu',input_shape=(1,18,64),use_bias=True))
    model.add(Flatten())
    model.add(Dense(units=1164,kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),activation='relu',input_dim=1152))
    #model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(units=100,kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),activation='relu',input_dim=1164))
    #model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(units=50,kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),activation='relu',input_dim=100))
    #model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(units=10,kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),activation='relu',input_dim=50))
    #model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(units=1,kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),input_dim=10))
    # model.add(Dense(units=4,kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),input_dim=10,activation='softmax'))
    #model.add(Activation('relu'))
    # model.add(Dropout(0.2))
    model.add(Lambda(atan_layer, output_shape = atan_layer_shape, name = "atan_0"))
    return model

def atan_layer (x) :
    return tf.multiply(tf.atan(x),2)

def atan_layer_shape(input_shape):
    return input_shape

def soft_acc (y_true , y_pred) :
    return K.mean(K.equal(K.round(y_true),K.round(y_pred)))
#sess = tf.InteractiveSession()
#saver = tf.train.Saver()model_retrained_acc_89model_retrained_acc_89model_retrained_acc_89model_retrained_acc_89
#saver.restore(sess, "save/model.ckpt")
model=getmodel()
model.load_weights('model_pretrained_credit_ta7t.h5')
#compile=True , custom_objects={'tf':tf,'atan_layer':atan_layer,'atan_layer_shape':atan_layer_shape,'soft_acc':soft_acc}
#dc=50
outAction = open('outAction.txt','a+')
#while(cv2.waitKey(10) != ord('q')):
count=0
start=time.clock()
#for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
while (True):    
    _,image_cap = cap.read()
    cv2.imwrite("image.jpg",image_cap)
    dummy=cv2.imread("image.jpg")
    # openCV code
    full_image = scipy.misc.imread("image.jpg", mode="RGB")
    count+=1
    image = scipy.misc.imresize(full_image[-150:], [66, 200]) / 255.0
    
#     if(stop.stop_condition(dummy)):
#         stop_FB()
# #        stopRL()
# #        time.sleep(5)
#         rawCapture.truncate(0)
#         continue
    

    image=np.expand_dims(image, axis=0)
    t1=time.clock()
#    awad=tf.argmax(tf.nn.softmax( model.y),dimension=1).eval(feed_dict={model.x: [image], model.keep_prob: 1.0})
   
    #awad=np.argmax(model.predict(image,batch_size=1))
    degrees=(model.predict(image,batch_size=1)*180/pi)
    t2=time.clock()
    print("img"+str(count)+": "+str(t2-t1))
    print(degrees)
#    degrees=(str(np.squeeze(awad))).strip('[')
#    degrees=degrees.strip(']')
#    print(degrees)
#    outAction.write(degrees +'\n')
#    call("clear")
    cv2.imshow("frame", cv2.cvtColor(full_image, cv2.COLOR_RGB2BGR))
    # clear the stream in preparation for the next frame
    degrees+=60
    forward(0.25)

    position(degrees)
#    delta
    time.sleep(0.5)
    stop()
#    stopRL()
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        stop()
        break

end=time.clock()
print("Total: " + str(count))
print("Duration: " + str(end-start))
 
outAction.close()
stop()
#stopRL()
action="end"
cap.release()
cv2.destroyAllWindows()
