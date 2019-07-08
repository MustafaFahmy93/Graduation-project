import cv2
import numpy as np
n=11306


xs=[]
l=[]
ys=[]
i=0
with open("out.txt") as f:
    for line in f:
        xs.append(line.split(' ')[0])
        #the paper by Nvidia uses the inverse of the turning radius,
        #but steering wheel angle is proportional to the inverse of turning radius
        #so the steering wheel angle in radians is used as the output
        ys.append(int(line.split()[1]))
        

textfile= open('out.txt', 'a')
for i in range(len(xs)) :
    if (ys[i] != 0):
        print(xs[i]+"\n")
        image=cv2.imread(xs[i])
        cv2.flip(image,1,image)
        cv2.imwrite(str(n)+".jpg",image)
        textfile.write(str(n)+".jpg"+" "+str(ys[i]*-1)+"\n")
        n+=1
    elif (ys[i] == 0):

        print(xs[i]+"\n")
        image=cv2.imread(xs[i])
        cv2.flip(image,1,image)
        cv2.imwrite(str(n)+".jpg",image)
        textfile.write(str(n)+".jpg"+" "+str(ys[i])+"\n")
        n+=1

textfile.close()
