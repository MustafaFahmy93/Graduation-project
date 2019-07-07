from pwm import *
inA1 = 0 # motor A in1
inA2 = 1 # motor A in2
inB = 2 # motor B  servo
#   motor A
set_pwm(inA1,0)
set_pwm(inA2,0)
inc = 40
right_flag,left_flag=0,0
#motor B(0.9ms-2.1ms) (50Hz-period=>20ms
set_pwm(inB,0)
def position(angel) : 
        x=((angel+60)*1.2/120.0)+0.9
        var=int((x/20)*4096)
        set_pwm(inB,var)
##        time.sleep(0.25)
       # print("theoneandonly servo angle= "+str(var))
        
        
def forward(dc):
    set_pwm(inA1,int(dc*4096))
    set_pwm(inA2,0)
def backward(dc):
    set_pwm(inA1,0)
    set_pwm(inA2,int(dc*4096))

def stop():
    set_pwm(inA1,0)
    set_pwm(inA2,0)


#position(60)
#time.sleep(1)

#position(0)
#time.sleep(1)

#position(-60)
#time.sleep(1)

#position(0)
#time.sleep(1)
