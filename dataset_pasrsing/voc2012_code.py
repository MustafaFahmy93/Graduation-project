import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import shutil
from os import path

classes = ["bicycle" ,"bus" ,"car", "cat", "chair", "dog", "motorbike", "person"]

sets = ['trainval']
#    , 'val' , 'trainval']

new_image_ids =[]
truth_grounds=[]
path_2012 = "E:/gradutaion_project/phase_2/data_sets/voc_2012/VOCdevkit/VOC2012"
path_2007 = "E:/gradutaion_project/phase_2/data_sets/voc_2007/VOCdevkit/VOC2007"

for the_class in classes:
    for image_set in sets:
        if not os.path.exists( path_2007+ '/labels/'):
            os.makedirs(path_2007 + '/labels/')
        if not os.path.exists( path_2007+ '/my_images/'):
            os.makedirs(path_2007 + '/my_images/')
        image_ids = open(path_2012+'/ImageSets/Main/%s_%s.txt'%(the_class, image_set)).read().strip().split()
        for image_id in image_ids[::2]:

            new_image_ids.append(image_id)
        for truth_ground in image_ids[1::2]:
            truth_grounds.append(truth_ground)



        for image_id ,truth_ground in zip (new_image_ids ,truth_grounds) :
            # print(image_id)
            # print(truth_ground)
            if truth_ground =='1' :
                print(image_id)
                src_l = path_2012 +'/annotations/'+image_id+'.xml'
                dst_l = path_2007 + '/labels/'+ image_id+'.xml'
                src_img=path_2012 + '/JPEGImages/' + image_id+'.jpg'
                dst_img=path_2007 + '/my_images/' + image_id + '.jpg'
                print(src_l, dst_l)
                shutil.copy(src_l, dst_l)
                shutil.copy(src_img, dst_img)







            #in_file = open('E:/gradutaion_project/phase_2/data_sets/VOC/VOCdevkit/VOC2012_Copy/Annotations/%s.xml' % ( '2008_000008'))

            # tree = ET.parse(in_file)

            #out_file = open('E:/gradutaion_project/phase_2/data_sets/VOC/VOCdevkit/VOC2012_Copy/labels/$s.xml' % ( image_id), 'w')


            # print(tree)




#E:/gradutaion_project/phase_2/data_sets/VOC/VOCdevkit/VOC2012_Copy