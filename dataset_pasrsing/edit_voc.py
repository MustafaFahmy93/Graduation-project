import os, sys, shutil, glob, argparse
import numpy as np
from PIL import Image
from lxml import etree
import xml.etree.ElementTree as ET 
classes = ["bicycle" ,"bus" ,"car", "cat", "chair", "dog", "motorbike", "person"]
for f in os.listdir("my_dataset/labels/"):
        #print(f)
        fname = ("my_dataset/labels/" + f)
        if os.path.isfile(fname):
            tree = ET.parse(fname)  
            annotation = tree.getroot()
            #print('Item #2 attribute:')  
           # print(annotation)
            for type_tag in annotation.findall('folder'):
                text1 = type_tag.text
                if text1 == 'VOC2007':
                    annotation.find('filename').text = '2007_' +  annotation.find('filename').text
                print(annotation.find('filename').text)
            
            for elem in annotation.findall('object'):
                elem1 = elem.find('name')
                if not (elem1.text in classes):
                    annotation.remove(elem)
            tree.write('file_new/'+ f)
