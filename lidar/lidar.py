from rplidar import RPLidar
import time

#function to map the pixels of the object to the angle of the object
def mapping_pix2angle(min_pixel, max_pixel):

    #width of the capture images = 1280 pixel
    #angle of the camera = 60
    min_angle = min_pixel*60/1280
    print(min_angle)
    max_angle = max_pixel*60/1280
    print(max_angle)
    centre = (min_angle+max_angle)/2
    # return the center angle of the object

    return centre


def object_depth_try(min, max):

    center_angle = mapping_pix2angle(min, max)

    #wide the range of the center angle

    min_angle = center_angle - 2
    max_angle = center_angle + 2

    try:
        #the address the lidar connected to COM5
        lidar = RPLidar('COM9')

        angleList = []
        distanceList = []

        i = 0
        objectDis = []
        for scan in lidar.iter_scans():
            # for loop to take the required range of the camera from 0 to 60
            for (_, angle, distance) in scan:
                if (angle >= 0 and angle <= 30) or (angle>=330 and angle<=360):
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
        #anglelist contain all the angles
        #distancelist contain distance at each angle

        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()



         #for loop to take distances of the object

        for i in range(len(angleList)):
            if angleList[i]>=min_angle and angleList[i]<=max_angle:
                objectDis.append(distanceList[i])
        #the average of the distances

        objectAvgDistance = sum(objectDis)/len(objectDis)

        return objectAvgDistance

    except:
        return None


def object_depth(min,max) :

    x = object_depth_try(min,max)
    while(x == None):
        print('error ')
        x = object_depth_try(min,max)
    return x



start = time.clock()



x = object_depth(240, 600)
end = time.clock ()

print(x)
print(end-start)



    # print(sum(objectAvgDis)/len(objectAvgDis))
    #
    # print(angleList)
    # print(distanceList)
    # print(len(angleList))
    # print(len(distanceList))
    #
    # lidar.stop()
    # lidar.stop_motor()
    # lidar.disconnect()
