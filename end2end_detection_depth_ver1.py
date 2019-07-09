#End to End ====================================================
import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]=""
#import tensrflow as tf
import keras 
import scipy.misc
#import model
import cv2
import numpy as np
from subprocess import call
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
from pynput import keyboard
#detection_lidar ====================================================
import json
from rplidar import RPLidar
import time
from darkflow.net.build import TFNet
# import video
import threading
thread = []
global_image=np.array([1])
interrupt = False
endtoendFlag= True
end_app = False
##############################cam_thread##########################
def cam_thread():
    global global_image,end_app
    cap = cv2.VideoCapture("/dev/video1")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,455)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,256)
    while (end_app==False):
        _,global_image = cap.read()
        cv2.imshow('global_image', global_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()
##############################End2End_functions##########################
def getmodel():
    model=Sequential()
    model.add(Conv2D(24,(5,5),strides=(2,2),kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),activation='relu',input_shape=(66,200,3),use_bias=True))
    model.add(Conv2D(36,(5,5),strides=(2,2),kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),activation='relu',input_shape=(31,98,24),use_bias=True))
    model.add(Conv2D(48,(5,5),strides=(2,2),kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),activation='relu',input_shape=(14,47,36),use_bias=True))
    model.add(Conv2D(64,(3,3),strides=(1,1),kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),activation='relu',input_shape=(5,22,48),use_bias=True))
    model.add(Conv2D(64,(3,3),strides=(1,1),kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),activation='relu',input_shape=(1,18,64),use_bias=True))
    model.add(Flatten())
    model.add(Dense(units=1164,kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),activation='relu',input_dim=1152))
    model.add(Dropout(0.2))
    model.add(Dense(units=100,kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),activation='relu',input_dim=1164))
    model.add(Dropout(0.2))
    model.add(Dense(units=50,kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),activation='relu',input_dim=100))
    model.add(Dropout(0.2))
    model.add(Dense(units=10,kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),activation='relu',input_dim=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1,kernel_initializer=TruncatedNormal(stddev=0.1),bias_initializer=Constant(value=0.1),input_dim=10))
    model.add(Lambda(atan_layer, output_shape = atan_layer_shape, name = "atan_0"))
    return model
def atan_layer (x) :
    return tf.multiply(tf.atan(x),2)

def atan_layer_shape(input_shape):
    return input_shape

def soft_acc (y_true , y_pred) :
    return K.mean(K.equal(K.round(y_true),K.round(y_pred)))
model=getmodel()
model.load_weights('model_pretrained_credit_ta7t.h5')
outAction = open('outAction.txt','a+')
count=0
start=time.clock()
################################End2EndThread########################
def end2endTread():
    global end_app,endtoendFlag,global_image,count
    while (end_app==False and endtoendFlag == True):
        cv2.imwrite("image.jpg",global_image)
        dummy=cv2.imread("image.jpg")
        # openCV code
        full_image = scipy.misc.imread("image.jpg", mode="RGB")
        count+=1
        image = scipy.misc.imresize(full_image[-150:], [66, 200]) / 255.0
        image=np.expand_dims(image, axis=0)
        t1=time.clock()
        degrees=(model.predict(image,batch_size=1)*180/pi)
        t2=time.clock()
        print("img"+str(count)+": "+str(t2-t1))
        print(degrees)
        cv2.imshow("global_image", cv2.cvtColor(full_image, cv2.COLOR_RGB2BGR))
        # clear the stream in preparation for the next global_image
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
################################Obj2lidar Thread#####################
def obj2lidar_thread():
    t = time.time()
    global result
    result = []
    options = {"model": "cfg/tiny-yolo-voc-3c.cfg", "load": -1, "threshold": 0.4,
            #"gpu": 1.0
            }
    tfnet = TFNet(options)
    def mapping_pix2angle(min_pixel, max_pixel):
        # width of the capture images = 1280 pixel
        # angle of the camera = 60
        min_angle = min_pixel*60/455
        # print(min_angle)
        max_angle = max_pixel*60/455
        # print(max_angle)
        centre = (min_angle+max_angle)/2
        # return the center angle of the object
        return centre
    def object_depth_try(min, max):
        center_angle = mapping_pix2angle(min, max)
        # wide the range of the center angle
        min_angle = center_angle - 2
        max_angle = center_angle + 2
        try:
            lidar = RPLidar('/dev/ttyUSB0')
            # the address the lidar connected to COM5
            #angleList = []
            distanceList = []
            i = 0
            #objectDis = []
            for scan in lidar.iter_scans():
                # for loop to take the required range of the camera from 0 to 60
                for (_, angle, distance) in scan:
                    if (angle >= 0 and angle <= 30) or (angle >= 330 and angle <= 360):
                        if (angle >= 0 and angle <= 30):
                            angle = angle + 30
                            #angleList.append(angle)
                            distanceList.append(distance/1000)
                        if (angle >= 330 and angle <= 360):
                            angle = angle - 330
                            #angleList.append(angle)
                            distanceList.append(distance/1000)
                i += 1
                if i > 1:
                    break
            # anglelist contain all the angles
            # distancelist contain distance at each angle

            lidar.stop()
            lidar.stop_motor()
            lidar.disconnect()

            # for loop to take distances of the object

            #for i in range(len(angleList)):
              #  if angleList[i] >= min_angle and angleList[i] <= max_angle:
               #     objectDis.append(distanceList[i])
            # the average of the distances

            objectAvgDistance = sum(distanceList)/len(distanceList)

            return objectAvgDistance

        except:
            return None


    def object_depth(min, max):

        x = object_depth_try(min, max)
        while(x == None):
            #print('error ')
            x = object_depth_try(min, max)
        return x


    # def detect(image, iter):
    #     global result
    #     # if iter % 1 == 0:
    #     result = tfnet.return_predict(image)
    #     print(result)

    def lidarthread():
        global end_app,endtoendFlag,global_image
        # global result
        # print(result)
        objects = []
        depthList = []
        # video = open('video')
        # iterator = 0
        # with open('123.json') as json_file:
        while (end_app==False):
            print('#############################################################')
    # 1
            # cv2.imwrite('video/'+str(iterator)+'.jpg', global_image)
            t0 = time.time()
            data = tfnet.return_predict(global_image)

            # print(data)
            
            for p in data:
                # print( p['topleft'])
                # print(p)
                x1 = p['topleft']['x']
                x2 = p['bottomright']['x']
                t = time.time()
                x = object_depth(x1, x2)
                end = time.time()
                # f = open('video/'+str(iterator)+'.txt', 'w')
                # f.write(p['label'] + " distance= " + str(x))
                # f.write(p['label'] + " time= " + str(end-t))
                print("Object Detected: ", p['label'], " with a distance= ", x, "\n")
                if x > 1.5 and x <= 2.5:
                    print('>>>>>WARNING!!!!!<<< \n >>SLOW DOWN<<\n')
                elif x <= 1.5:
                    print('>>>>>WARNING!!!!!<<< \n >>STOP<<\n')
                    endtoendFlag=False
                    stop()
                # depth = object_depth(x1, x2)
                objects.append(p['label'])
                # iterator += 1
                # depthList.append(depth)
            end0 = time.time()
    lidarthread()
# ================================================
def listen_key_Thread():
    def on_press(key):
        global interrupt, end_app,endtoendFlag
        interrupt = True
        endtoendFlag=False
        print("Pilot")
        dc = 0.6
        if (key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
            print("forword")
            forward(dc)
            position(0)
        elif (key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
            print("backword")
            backward(dc)
        elif (key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):
            print("right")
            position(60)
        elif (key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
            print("left")
            position(-60)
        elif (key == keyboard.KeyCode(char='b')):
            end_app = True
            stop()
            print("stop")
            exit(0)

    def on_release(key):
        global interrupt,endtoendFlag
        interrupt = False
        endtoendFlag = True
        if (key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
            stop()
        elif (key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
            stop()
        elif (key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):
            stop()
        elif (key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
            stop()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


t1 = threading.Thread(target=cam_thread, args=[])
t2 = threading.Thread(target=listen_key_Thread, args=[])
t3 = threading.Thread(target=end2endTread,args=[])
t4 = threading.Thread(target=obj2lidar_thread,args=[])

t1.start()
t2.start()
t3.start()
t4.start()