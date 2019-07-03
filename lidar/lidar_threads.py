from rplidar import RPLidar
import time
import threading
thread = []
lidar = RPLidar('/dev/ttyUSB0')
ret_dist=0
req_angle=0
flag=0
def lidarThread():
        global ret_dist,req_angle,flag
        #global lidar
        while(req_angle!=404):
                try:
                        info = lidar.get_info()
                        print(info)

                        health = lidar.get_health()
                        print(health)
                        for i, scan in enumerate(lidar.iter_scans(max_buf_meas=1000)):
                                #print('%d: Got %d measurments' % (i, len(scan)))
                                #print(len(scan))
                                for (_, angle, distance) in scan:
                                        if(flag==0):
                                                continue
                                        if (angle >= 0 and angle <= 30) or (angle>=330 and angle<=360):
                                                if(req_angle>(req_angle-2) and req_angle<(req_angle+2)):
                                                        #return distance
                                                        ret_dist=distance/1000
                except:
                        print('ERROR')
                        

        

def main_test_Thread():
        global ret_dist,req_angle,flag
        req_angle=0
        while(req_angle!=404):

                req_angle=int(input("enter your angle"))
                flag=1
                t1=time.clock()
                while(ret_dist==0):
                         x=0
                print(ret_dist)
                flag=0
                ret_dist=0
                # while(ret_dist!=None):
                #         x=lidarThread(req_angle)
                # print(x)
                t2=time.clock()
                print(t2-t1)
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()


t1 = threading.Thread(target=lidarThread, args=[])
t2 = threading.Thread(target=main_test_Thread, args=[])

# lidar.stop()
# lidar.stop_motor()
# lidar.disconnect()

t2.start()
t1.start()