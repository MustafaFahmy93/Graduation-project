from darkflow.net.build import TFNet
import cv2

options = {"model": "cfg/tiny-yolo-voc-3c.cfg", "load": -1, "threshold": 0.2
,
#'gpu': 1.0,
'allow_growth':True
}

tfnet = TFNet(options)

result = ''
def detect(image, iter):
    global result
    if iter % 50 == 0:
        result = tfnet.return_predict(image)
        print(result)


cap = cv2.VideoCapture("/dev/video1")
#cap = cv2.VideoCapture(1)
iterator = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here

    detect(frame, iterator)
    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    iterator += 1

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
