import serial
import string
import pynmea2
port = "/dev/ttyTHS2"
ser = serial.Serial(port, baudrate=9600, timeout=0.5)


def gps_lat_lon():
   # Yasmin (GPS Warmup)
        newdata = ser.readline()
        try:
            data = newdata.decode().split(",")

            #print(data)
            if (data[0] == "$GPRMC"):
                # print(newdata)
                # print(data[5])
                #print(data[2])
                if(data[2] == "A"):
                    if((data[5] != " ")and data[3] != " "):
                        lat = float(data[3])
                        lon = float(data[5])
                        lat1 = int(lat/100)
                        lon1 = int(lon/100)
                        s1 = (float(str(lat)[2:])/60)+lat1
                        s2 = (float(str(lon)[2:])/60)+lon1
                        latlon = []
                        latlon.append(s1)
                        latlon.append(s2)
                        if(s1 != None):
                            return latlon
        except:
            return None
