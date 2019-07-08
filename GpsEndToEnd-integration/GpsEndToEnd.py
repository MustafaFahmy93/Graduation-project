import gps
import threading
import run_gps_edit as gps
from run_big import *
from pynput import keyboard
from firebase import Firebase
Thread=[]



angle_global=0
position_global=0
endToEndFlag=True

def gpsThread():
    global angle_global
    global endToEndFlag
    print("inside gpsthread ")
    gps.rungpsnw()


def endToEndThread():
    model=getmodel()
    model.load_weights('model_pretrained_credit_ta7t.h5')
    #compile=True , custom_objects={'tf':tf,'atan_layer':atan_layer,'atan_layer_shape':atan_layer_shape,'soft_acc':soft_acc}
    #dc=50
    outAction = open('outAction.txt','a+')
    #while(cv2.waitKey(10) != ord('q')):
    count=0
    start=time.clock()
    #for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):

    global endToEndFlag
    while (endToEndFlag):
        _,image_cap = cap.read()
        cv2.imwrite("image.jpg",image_cap)
        dummy=cv2.imread("image.jpg")
        # openCV code
        full_image = scipy.misc.imread("image.jpg", mode="RGB")
        count+=1
        image = scipy.misc.imresize(full_image[-150:], [66, 200]) / 255.0
        
    #     if(stop.stop_condition(dummy)):
    #         stop_FB()
    # #        stopRL()
    # #        time.sleep(5)
    #         rawCapture.truncate(0)
    #         continue
        

        image=np.expand_dims(image, axis=0)
        t1=time.clock()
    #    awad=tf.argmax(tf.nn.softmax( model.y),dimension=1).eval(feed_dict={model.x: [image], model.keep_prob: 1.0})
       
        #awad=np.argmax(model.predict(image,batch_size=1))
        degrees=(model.predict(image,batch_size=1)*180/pi)
        t2=time.clock()
#        print("img"+str(count)+": "+str(t2-t1))
        print(degrees)
    #    degrees=(str(np.squeeze(awad))).strip('[')
    #    degrees=degrees.strip(']')
    #    print(degrees)
    #    outAction.write(degrees +'\n')
    #    call("clear")
        cv2.imshow("frame", cv2.cvtColor(full_image, cv2.COLOR_RGB2BGR))
        # clear the stream in preparation for the next frame
        degrees+=60
        forward(0.27)

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





def listen_key_Thread():
    def on_press(key):
        global interrupt
        interrupt= True
        print("Pilot")
        if(key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
            print("forword")
        elif(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
            print("backword")
        elif(key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):
            print("right")
        elif(key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
            print("left")
        elif(key == keyboard.KeyCode(char='h')):
            if(dc!=100):
                dc=(dc+10)%110
            print(dc)
        elif(key == keyboard.KeyCode(char='l')):
            if(dc!=0):
                dc=(dc-10)%100
            print(dc)
        elif(key == keyboard.KeyCode(char='b')):
            exit(0)

    def on_release(key):
        global interrupt
        interrupt= False
        if(key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
            print("release_forword")
        elif(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
            print("release_backword")
        elif(key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):
            print("release_right")
        elif(key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
            print("release_left")

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()



t1=threading.Thread(target=gpsThread,args=[])
t2=  threading.Thread(target=endToEndThread,args=[])
t3 = threading.Thread(target=listen_key_Thread, args=[])
#t4 = threading.Thread(target=compass, args=[])
t1.start()
t2.start()
t3.start()
#t4.start()
