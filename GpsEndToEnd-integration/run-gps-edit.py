'''
map verison 10
find shortest path & nearest nodes from the start point (ver2) (start point out of line) & draw (map (college) & path)
& multithreading & car control (GPS & keyboard)
'''
import coordinates as co  # map
from math import sin, cos, sqrt, atan2, radians, degrees, acos
import time
from sys import exit
from pynput import keyboard
import threading
#import gps
import serial
import string
import pynmea2
#import QMCcompass
#from compass import *
#from hmc5883l import *
from ctrl import *
from firebase import Firebase


#GPS_lat = db.child("GPS").child("lat").get().val()
#GPS_long = db.child("GPS").child("long").get().val()

#Compass_head = db.child("Compass").child("head").get().val()
#Compass_x = db.child("Compass").child("x").get().val()
#Compass_y = db.child("Compass").child("y").get().val()
#Compass_z = db.child("Compass").child("z").get().val()

#print(GPS_lat,GPS_long)
#print(Compass_head,Compass_x,Compass_y,Compass_z)
thread = []
interrupt = False
end_app = False
angle_global=0
global_position=[0,0]
##############################functions##########################
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
    
    #GPS_lat = db.child("GPS").child("lat").get().val()
    #GPS_long = db.child("GPS").child("long").get().val()
        #position_global=[GPS_lat,GPS_long]
port="/dev/ttyTHS2" ##Nvidia J17
#port="/dev/ttyAMA0"
ser=serial.Serial(port,baudrate=9600,timeout=0.5 )
def compass():
    print("inside compasss  nmwww")
    global angle_global
    global global_poistion
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
    while(True):
        angle_global= db.child("Compass").child("head").get().val()

#        GPS_lat = db.child("GPS").child("lat").get().val()
#        GPS_long = db.child("GPS").child("long").get().val()
#        position_global=[GPS_lat,GPS_long]



def gps_lat_lon():
    global global_position,end_app
   #Yasmin (GPS Warmup)

    newdata= ser.readline()
   #print(newdata)
    while(end_app==False):
        try:     
            data=newdata.decode().split(",")
            #print(data[0])
            if (data[0]=="$GPRMC"):
                #print(newdata)
                #print(data[5])
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
                            #print(global_position)
        except:
            global_position = None
#def gpsThread():
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
    # print("The distance is %.2fkm." % dist)

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

################################__main__##########################
def rungpsnw():
    global interrupt, end_app,angle_global,global_position
    global endToEndFlag
    endToEndFlag=True 

    # load map
    graph = co.graph
    coordinates = co.coordinates
    # fine_path
    #j = 0  # Yasmin (GPS Warmup)
    #for j in range(10):
    #    j += 1
    #    gps.gps_lat_lon()  # Yasmin
    current_position = None
    #print("here")
    while current_position == None:
        current_position = global_position#gps.gps_lat_lon()  # [30.064091, 31.279413]
        #print(global_position)
        #print("gps")
    #while compass() == None:
     #   x=0
        #current_position = gps.gps_lat_lon()  # [30.064091, 31.279413]

    candidate_nodes = nearest_nodes(current_position, graph, coordinates)
    start = candidate_nodes[0]
    goal_state = 'W'
    gps_file=open("gps.txt",'a+')
    compass_file=open("compass.txt",'a+')
    gps_file.write(goal_state+"\n")
    compass_file.write(goal_state+"\n")
    if (total_distance(current_position, find_shortest_path(graph, candidate_nodes[0], goal_state),
                       coordinates) > total_distance(current_position,
                                                     find_shortest_path(graph, candidate_nodes[1], goal_state), coordinates)):
        start = candidate_nodes[1]
    path = find_shortest_path(graph, start, goal_state)
    print(path)
    i = 0
    count_next=0
    dc = 0.6

    while (True):
    #    time.sleep(0.5)
        
        current_position = global_position#gps.gps_lat_lon()  # [30.064091, 31.279413]##from gps module

        current_angle =angle_global#compass()
        if current_position == None or current_angle == None:
            #stop()
            continue
        gps_file.write(str(current_position[0])+","+str(current_position[1])+"\n")
        print("distance=> " + path[i] + "(" + str(distance(current_position, coordinates[path[i]])) + ")")
        des_angle = angleBtn2Coordinates(current_position, coordinates[path[i]])

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
        if ((interrupt == False) and (endToEndFlag==False)):
            # print("autopilot")
            #print("angle_servo=> " + str(req_angle))
            print("distance=> " + path[i] + "(" + str(distance(current_position, coordinates[path[i]])) + ")")
            print("not "+str(des_angle))
            print("Compass "+str(current_angle))
            # servo(req_angle)
            position(req_angle)
            # motors(forword)
        
            forward(dc)
            time.sleep(0.5)
            stop()
        if (end_app):
            stop()
            print("break")
            break

        if (distance(current_position, coordinates[path[i]]) > 2):
            dc = 1
            endToEndFlag=True
            print("high speed")


        elif ((distance(current_position, coordinates[path[i]]) < 2) and (i + 1 < len(path))):
            count_next+=1
            if(count_next==3):
                dc = 0.8 
                print(path[i:])
                i += 1  # next state
                count_next=0
                endToEndFlag=False
                print("less than 2m")
        elif((distance(current_position,coordinates[path[i-1]])>2) and (i+1 < len(path)) and i > 0):
                endToEndFlag=True
                print("goooooo end to end")
        elif ((distance(current_position, coordinates[path[i]]) < 2) and (i + 1 == len(path))):  # i+1 last state
            ##stop
            count_next+=1
            if(count_next==3):
                print("Congratulations!")
                stop()
                break

    gps_file.close()
    compass_file.close()
    exit(0)

#            break

#if __name__ == "__main__":
#    main()



#t1 = threading.Thread(target=gpsThread, args=[])
#t2 = threading.Thread(target=compass, args=[])

#t2.start()
#t1.start()

t1=threading.Thread(target=gps_lat_lon,args=[])
t2=  threading.Thread(target=compass,args=[])
t1.start()
t2.start()
