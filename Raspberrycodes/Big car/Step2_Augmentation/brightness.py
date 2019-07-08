import cv2
import numpy as np
n=22613

xs=[]
l=[]
ys=[]
i=0

def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):

    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow

        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()

    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf

f = open("out.txt","r")
for line in f:
	xs.append(line.split(' ')[0])

	ys.append(int(line.split(' ')[1]))
    #i+=4


tt = open("data.txt", "a+")
for j in range(len(xs)) :
        image=cv2.imread(xs[j])
        edited_image=apply_brightness_contrast(image,-50,40)
        cv2.imwrite(str(n)+".jpg",edited_image)
        tt.write(str(n)+".jpg "+" "+str(ys[j])+"\n")
        n+=1

tt.close()
print(n)
