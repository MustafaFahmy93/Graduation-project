
import time
import hmc5883l


def compass():

    try:
        sensor = hmc5883l.hmc5883l(gauss = 8.1, declination = (4,32))
        result = sensor.degrees(sensor.heading())[0]#
        time.sleep(0.01)
        return result
    except:
        return None


while(True):
    print(compass())
    time.sleep(0.5)
