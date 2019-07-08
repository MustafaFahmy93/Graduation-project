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
#GPS & Compass ====================================================
import coordinates as co  # map
from math import sin, cos, sqrt, atan2, radians, degrees, acos
import time
from sys import exit
from pynput import keyboard
import threading
from ctrl import *
from firebase import Firebase
import serial
import string
import pynmea2
thread = []
interrupt = False
endtoendFlag= False
end_app = False
angle_global=0
global_position=0
##############################compass##########################
def compass():
    global angle_global,end_app
    config = {
        "apiKey": "AIzaSyDZQENVi3p5rZZwC8YaA4tfeB8kFo9bLgA",
        "authDomain": "igp-sensors-readings.firebaseapp.com",
        "databaseURL": "https://igp-sensors-readings.firebaseio.com",
        "projectId": "igp-sensors-readings",
        "storageBucket": "igp-sensors-readings.appspot.com",
        "messagingSenderId": "699634168979",
        "appId": "1:699634168979:web:df476c33c6f57180"
      }
    firebase = Firebase(config)
    db = firebase.database()
    while(end_app==False):
        angle_global= db.child("Compass").child("head").get().val()
##############################GPS##########################
def gps_lat_lon():
    global global_position,end_app
    newdata= ser.readline()
    while(end_app==False):
        try:     
            data=newdata.decode().split(",")
            if (data[0]=="$GPRMC"):
                if(data[2]=="A"):
                    if((data[5]!=" ")and data[3]!=" "):
                        lat=float(data[3])
                        lon=float(data[5])
                        lat1=int(lat/100 )
                        lon1=int(lon/100 )      
                        s1=(float(str(lat)[2:])/60 )+lat1
                        s2=(float(str(lon)[2:])/60 )+lon1
                        latlon=[]
                        latlon.append(s1)
                        latlon.append(s2)
                        if(s1!= None):
                            global_position = latlon
        except:
            global_position = None

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
    global end_app,endtoendFlag
    while (end_app==False and endtoendFlag == True):    
        _,image_cap = cap.read()
        cv2.imwrite("image.jpg",image_cap)
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
##############################GPS_functions##########################
def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    ##        if not graph.has_key(start):
    ##            return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest
def distance(a, b):
    slat = radians(a[0])
    slon = radians(a[1])
    elat = radians(b[0])
    elon = radians(b[1])
    dist = 6371.01 * acos(sin(slat) * sin(elat) + cos(slat) * cos(elat) * cos(slon - elon))
    return (dist * 1000)
def nearest_nodes(C, graph, coordinates):
    min = 10000000
    n1 = 'x'
    n2 = 'x'
    for p in graph:
        for node_p in graph[p]:
            dist = (distance(C, coordinates[p]) + distance(C, coordinates[node_p])) - (
                distance(coordinates[p], coordinates[node_p]))
            if (min > dist):
                min = dist
                n1 = p
                n2 = node_p
    return n1 + n2
def angleBtn2Coordinates(c1, c2):
    lat1, long1 = c1
    lat2, long2 = c2
    lat1 = radians(lat1)
    long1 = radians(long1)
    lat2 = radians(lat2)
    long2 = radians(long2)
    dlon = long2 - long1
    y = sin(dlon) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
    brng = atan2(y, x)
    brng = degrees(brng)
    brng = (brng + 360) % 360
    #brng = 360 - brng # count degrees counter-clockwise - remove to make clockwise
    return brng
def total_distance(current_position, path, coordinates):
    total = distance(current_position, coordinates[path[0]])
    for i in range(len(path)):
        if (i + 1 < len(path)):
            total = total + distance(coordinates[path[i]], coordinates[path[i + 1]])
    return int(total)
################################GPSThread########################################
def gpsThread():
    global interrupt,endtoendFlag, end_app,angle_global,position_global
    # load map
    graph = co.graph
    coordinates = co.coordinates
    # find_path
    current_position = None
    while current_position == None:
        current_position = global_position#gps.gps_lat_lon()  # [30.064091, 31.279413
    candidate_nodes = nearest_nodes(current_position, graph, coordinates)
    start = candidate_nodes[0]
    goal_state = 'B'
    gps_file=open("gps.txt",'a+')
    compass_file=open("compass.txt",'a+')
    gps_file.write(goal_state+"\n")
    compass_file.write(goal_state+"\n")
    dist_node1=total_distance(current_position, find_shortest_path(graph, candidate_nodes[0], goal_state),coordinates)
    dist_node2=total_distance(current_position,find_shortest_path(graph, candidate_nodes[1], goal_state), coordinates)
    if (dist_node1 > dist_node2):
        start = candidate_nodes[1]
    path = find_shortest_path(graph, start, goal_state)
    print(path)
    i = 0
    count_next=0
    dc = 0.6

    while (True):
        current_position = global_position#gps.gps_lat_lon()  # [30.064091, 31.279413]##from gps module

        current_angle =angle_global#compass()
        if current_position == None or current_angle == None:
            #stop()
            continue
        gps_file.write(str(current_position[0])+","+str(current_position[1])+"\n")
        compass_file.write(str(current_angle)+"\n")
        des_angle = angleBtn2Coordinates(current_position, coordinates[path[i]])
        print("distance=> " + path[i] + "(" + str(distance(current_position, coordinates[path[i]])) + ")")
        print("not "+str(des_angle))
        print("Compass "+str(current_angle))
        #current_angle=180-(current_angle%180)    
        req_angle = des_angle - current_angle
        if ((req_angle)>180):
            req_angle=(abs(req_angle))-360
        elif ((req_angle)<-180):
            req_angle=360-(abs(req_angle)) 

        if (req_angle > 60):
            req_angle = 60
        elif (req_angle < -60):
            req_angle = -60
        if ((interrupt == False) and (endToEndFlag == False)):
            # print("autopilot")
            print("angle_servo=> " + str(req_angle))
            #servo(req_angle)
            position(req_angle)
            #motors(forword)
            forward(dc)
            time.sleep(0.5)
            stop()
        if (end_app):
            stop()
            print("break")
            break

        if (distance(current_position, coordinates[path[i]]) > 3):
            dc = 1
            endToEndFlag=True
        elif ((distance(current_position, coordinates[path[i]]) < 3) and (i + 1 < len(path))):
            count_next+=1
            if(count_next==3):
                dc = 0.8 
                print(path[i:])
                i += 1  # next state
                count_next=0
                endToEndFlag=False
        elif((distance(current_position,coordinates[path[i-1]])>2) and (i+1 < len(path)) and i > 0):
                endToEndFlag=True
                print("go end to end")
        elif ((distance(current_position, coordinates[path[i]]) < 3) and (i + 1 == len(path))):  # i+1 last state
            ##stop
            count_next+=1
            if(count_next==3):
                print("Congratulations!")
                stop()
                break

    gps_file.close()
    compass_file.close()



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


t1 = threading.Thread(target=end2endTread,args=[])
t2 = threading.Thread(target=listen_key_Thread, args=[])
t3 = threading.Thread(target=gps_lat_lon,args=[])
t4 = threading.Thread(target=compass, args=[])
t5 = threading.Thread(target=gpsThread, args=[])

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()