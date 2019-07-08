from pynput import keyboard

def on_press(key):
        global dc,t1,thread
        global action
        global count,end,right_flag,left_flag
        if(key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
            #forward(dc)
##            position( 40 ,dc)
            global inc
            inc = 40
            action=inc - 40
        if(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
            #backward(dc)
            action="60"
        if(key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):
            global flag
            global inc
            right_flag=1

        if(key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
            global inc
            left_flag=1 
        if(key == keyboard.KeyCode(char='h')):
            if(dc!=100):
                dc=(dc+10)%110
            print(dc)
        if(key == keyboard.KeyCode(char='l')):
            if(dc!=0):
                dc=(dc-10)%100
            print(dc)
        if(key == keyboard.KeyCode(char='b')):
##            print ("stop-+6")
##            count_file = open ('count.txt',"w")
##            count_file.write(str(count))
##            count_file.close()
##            print(count)
            end=True
            time.sleep(2)
            #stop()
            #GPIO.cleanup()  
            exit(0)

def on_release(key):
        global flag,right_flag,left_flag
        flag = 0
        if(key == keyboard.Key.up or key == keyboard.KeyCode(char='w')):
            print("up stop")
            #stop()
        elif(key == keyboard.Key.down or key == keyboard.KeyCode(char='s')):
            print("down stop")
            #stop()
        elif(key == keyboard.Key.right or key == keyboard.KeyCode(char='d')):
            print("r stop")
            right_flag=0
            #stop() 
        elif(key == keyboard.Key.left or key == keyboard.KeyCode(char='a')):
            print("l stop")
            left_flag=0
            #stop()

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:      
	listener.join()
        
