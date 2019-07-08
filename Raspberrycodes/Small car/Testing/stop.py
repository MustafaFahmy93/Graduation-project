import cv2
import numpy as np

def nothing(x):
    pass
def stop_condition(frame):

    # cv2.namedWindow("Trackbars")

    # cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
    # cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
    # cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
    # cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
    # cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
    # cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)


    #while True:

        #_, frame = cap.read()
        #bgr =cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        hsv =cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # l_h = cv2.getTrackbarPos("L - H", "Trackbars")
        # l_s = cv2.getTrackbarPos("L - S", "Trackbars")
        # l_v = cv2.getTrackbarPos("L - V", "Trackbars")
        # u_h = cv2.getTrackbarPos("U - H", "Trackbars")
        # u_s = cv2.getTrackbarPos("U - S", "Trackbars")
        # u_v = cv2.getTrackbarPos("U - V", "Trackbars")

        lower_blue = np.array([25, 129, 0])
        upper_blue = np.array([179, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        avg=np.mean(mask)
        print(avg)
        if avg>97:
            return True

        else: 
            return False



        # key = cv2.waitKey(1)
        # if key == 27:
        #     break


    #cv2.destroyAllWindows()
