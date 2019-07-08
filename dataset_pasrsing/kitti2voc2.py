# Import necessary libraries
import os, sys, shutil, glob, argparse
import numpy as np
from PIL import Image
from lxml import etree

python_version = sys.version_info.major


###########################################################
##########        KITTI to VOC Conversion        ##########
###########################################################
def write_voc_file(fname, labels, coords, img_width, img_height):
    """
    Definition: Writes label into VOC (XML) format.
    Parameters: fname - full file path to label file
                labels - list of objects in file
                coords - list of position of objects in file
                img_width - width of image
                img_height - height of image
    Returns: annotation - XML tree for image file
    """
    annotation = etree.Element('annotation')
    folder = etree.Element('folder')
    filename = etree.Element('filename')
    f = fname.split("/")
    filename.text = f[-1]
    folder.text = "/".join(f[:-1])
    annotation.append(folder)

    annotation.append(filename)
    img_size = etree.Element('size')
    annotation.append(img_size)
    depth = etree.Element('depth')
    depth.text = '3'
    img_size.append(depth)
    height = etree.Element('height')
    height.text = str(img_height)
    img_size.append(height)
    width = etree.Element('width')
    width.text = str(img_width)
    img_size.append(width)

    for i in range(len(coords)):
        name = etree.Element('name')
        if labels[i] == 'Pedestrian':
            name.text = 'Person'
        elif labels[i] == 'cyclist':
            name.text = 'bicycle'
        elif labels[i] == 'DontCare':
            continue
        elif labels[i] == 'Misc':
            continue

        else:
            name.text = labels[i]
        object = etree.Element('object')
        annotation.append(object)

        object.append(name)
        pose = etree.Element('pose')
        pose.text = 'Unspecified'
        object.append(pose)
        truncated = etree.Element('truncated')
        truncated.text = '1'
        object.append(truncated)
        difficult = etree.Element('difficult')
        difficult.text = '0'
        object.append(difficult)
        bndbox = etree.Element('bndbox')
        object.append(bndbox)
        xmax = etree.Element('xmax')
        xmax.text = str(coords[i][2])
        bndbox.append(xmax)
        xmin = etree.Element('xmin')
        xmin.text = str(coords[i][0])
        bndbox.append(xmin)
        ymax = etree.Element('ymax')
        ymax.text = str(coords[i][3])
        bndbox.append(ymax)
        ymin = etree.Element('ymin')
        ymin.text = str(coords[i][1])
        bndbox.append(ymin)
        occluded = etree.Element('occluded')
        occluded.text = '0'
        object.append(occluded)

    return annotation


def parse_labels_voc(label_file):
    """
    Definition: Parses label file to extract label and bounding box
        coordintates.
    Parameters: label_file - list of labels in images
    Returns: all_labels - contains a list of labels for objects in the image
             all_coords - contains a list of coordinates for objects in image
    """
    lfile = open(label_file)
    coords = []
    all_coords = []
    all_labels = []
    for line in lfile:
        l = line.split(" ")
        all_labels.append(l[0])
        coords = list(map(int, list(map(float, l[4:8]))))
        xmin = coords[0]
        ymin = coords[1]
        xmax = coords[2]
        ymax = coords[3]
        tmp = [xmin, ymin, xmax, ymax]
        all_coords.append(list(map(int, tmp)))
    lfile.close()
    return all_labels, all_coords


def copy_images_voc(kitti, voc):
    """
    Definition: Copy all images from the training and validation sets
        in kitti format to training and validation image sets in voc
        format.
    Parameters: kitti - path to kitti directory (contains 'train' and 'val')
                voc - path to voc output directory
    Returns: None
    """
    for filename in glob.glob(os.path.join(kitti + "training/images/", "*.*")):
        shutil.copy(filename, voc + "train/images/")


def make_voc_directories(voc):
    """
    Definition: Make directories for voc images and labels.
        Removes previously created voc image and label directories.
    Parameters: yolo - path to voc directory to be created
    Returns: None
    """
    if os.path.exists(voc):
       shutil.rmtree(voc)
    os.makedirs(voc)
    os.makedirs(voc + "train")
    os.makedirs(voc + "train/images")
    os.makedirs(voc + "train/labels")


def voc(kitti_dir, voc_dir, label=None):
    print("Convert kitti to voc")

    # Make all directories for voc dataset
    make_voc_directories(voc_dir)

    # Iterate through kitti training data
    for f in os.listdir(kitti_dir + "training/labels/"):
        fname = (kitti_dir + "training/images/" + f).split(".txt")[0] + ".png"
        if os.path.isfile(fname):
            img = Image.open(fname)
            w, h = img.size
            img.close()
            labels, coords = parse_labels_voc(os.path.join(kitti_dir +
                                                           "training/labels/" + f))
            annotation = write_voc_file(fname, labels, coords, w, h)
            et = etree.ElementTree(annotation)
            et.write(voc_dir + "train/labels/" + f.split(".txt")[0] + ".xml", pretty_print=True)

    copy_images_voc(kitti_dir, voc_dir)


# first kitti path
# second desired name for voc folder
voc('E:/gradutaion_project/phase_2/data_sets/kittie/kitti/', 'E:/gradutaion_project/phase_2/data_sets/kittie/voc/')
