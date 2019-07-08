import json
from lidar import *
import cv2
# from rplidar import RPLidar
import time
from darkflow.net.build import TFNet
# import video
import threading
start = time.time()
# lidar = RPLidar('COM8')
# thread = []
global result
result = []


options = {"model": "cfg/tiny-yolo-voc-3c.cfg", "load": -1, "threshold": 0.2,
           "gpu": 1.0
           }

tfnet = TFNet(options)


def mapping_pix2angle(min_pixel, max_pixel):

    # width of the capture images = 1280 pixel
    # angle of the camera = 60
    min_angle = min_pixel*60/640
    # print(min_angle)
    max_angle = max_pixel*60/640
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
        # the address the lidar connected to COM5
        lidar = RPLidar('/dev/ttyUSB0')

        angleList = []
        distanceList = []

        i = 0
        objectDis = []
        for scan in lidar.iter_scans():
            # for loop to take the required range of the camera from 0 to 60
            for (_, angle, distance) in scan:
                if (angle >= 0 and angle <= 30) or (angle >= 330 and angle <= 360):
                    if (angle >= 0 and angle <= 30):
                        angle = angle + 30
                        angleList.append(angle)
                        distanceList.append(distance/1000)
                    if (angle >= 330 and angle <= 360):
                        angle = angle - 330
                        angleList.append(angle)
                        distanceList.append(distance/1000)
            i += 1
            if i > 3:
                break
        # anglelist contain all the angles
        # distancelist contain distance at each angle

        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()

        # for loop to take distances of the object

        for i in range(len(angleList)):
            if angleList[i] >= min_angle and angleList[i] <= max_angle:
                objectDis.append(distanceList[i])
        # the average of the distances

        objectAvgDistance = sum(objectDis)/len(objectDis)

        return objectAvgDistance

    except:
        return None


def object_depth(min, max):

    x = object_depth_try(min, max)
    while(x == None):
        print('error ')
        x = object_depth_try(min, max)
    return x


# def detect(image, iter):
#     global result
#     # if iter % 1 == 0:
#     result = tfnet.return_predict(image)
#     print(result)


def camthread():
    global result
    cap = cv2.VideoCapture(0)
    iterator = 0
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        result = tfnet.return_predict(frame)
        print(result)

        # detect(frame, iterator)
        # Display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        iterator += 1

# When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def lidarthread():
    # global result
    # print(result)
    objects = []
    depthList = []
    cap = cv2.VideoCapture(0)

    # with open('123.json') as json_file:
    while True:
        ret, frame = cap.read()
        start0 = time.clock()
        data = tfnet.return_predict(frame)
        # print(data)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        for p in data:
            # print( p['topleft'])
            print(p)
            x1 = p['topleft']['x']
            x2 = p['bottomright']['x']
            start = time.clock()
            x = object_depth(x1, x2)
            end = time.clock()
            print(p['label'], " distance=", x)
            print(p['label'], " time=", end-start)

            # depth = object_depth(x1, x2)
            objects.append(p['label'])
            # depthList.append(depth)
        end0 = time.clock()
        cv2.imshow('frame', frame)
        print("TIME ", end0-start0)

# lidar.stop()
# lidar.stop_motor()
# lidar.disconnect()
    #
    # print(objects)
    # print(depthList)
    # end = time.time()
    # print(end - start)


# t1 = threading.Thread(target=camthread, args=[])
# t2 = threading.Thread(target=lidarthread, args=[])
# t1.start()
# t2.start()
lidarthread()
