import shutil



path_kitti_images = 'E:\\gradutaion_project\\phase_2\\data_sets\\kittie\\kitti\\images\\'
path_kitti_labels = 'E:\\gradutaion_project\\phase_2\\data_sets\\kittie\\kitti\\labels\\'
path_images_dist = 'E:\\gradutaion_project\\phase_2\\data_sets\\kittie\\my_kitti\\images\\'
path_labels_dist = 'E:\\gradutaion_project\\phase_2\\data_sets\\kittie\\my_kitti\\labels\\'
my_objects= ['Car' , 'Cyclist' , 'Pedestrian' , 'Truck']
global in_my
in_my = False
def check_object(object):
    global in_my
    if  object in my_objects :
        print(object)
        in_my = True




for id in range (7481):

    in_my = False
    if (id < 10):
        src_l = path_kitti_labels + '00000' + str(id) + '.txt'
        src_img = path_kitti_images + '00000' + str(id) + '.png'
        dst_l = path_labels_dist + '00000' + str(id) + '.txt'
        dst_img = path_images_dist + '00000' + str(id) + '.png'

    elif (id < 100):
        src_l = path_kitti_labels + '0000' + str(id) + '.txt'
        src_img = path_kitti_images + '0000' + str(id) + '.png'
        dst_l = path_labels_dist + '0000' + str(id) + '.txt'
        dst_img = path_images_dist + '0000' + str(id) + '.png'

    elif (id < 1000):
        src_l = path_kitti_labels + '000' + str(id) + '.txt'
        src_img = path_kitti_images + '000' + str(id) + '.png'
        dst_l = path_labels_dist + '000' + str(id) + '.txt'
        dst_img = path_images_dist + '000' + str(id) + '.png'

    else:
        src_l = path_kitti_labels + '00' + str(id) + '.txt'
        src_img = path_kitti_images + '00' + str(id) + '.png'
        dst_l = path_labels_dist + '00' + str(id) + '.txt'
        dst_img = path_images_dist + '00' + str(id) + '.png'

    #src_l = path_kitti_labels + '00000' + '1' + '.txt'
    #src_img = path_kitti_images + '00000' + '1' + '.png'



    data_lines = open (src_l).read().split('\n')


    for line_no in range (len(data_lines)-1):
        line = data_lines[line_no].split()
        check_object(line[0])

    if in_my:

        shutil.copy(src_l, dst_l)
        data = open(dst_l, 'r')
        data_lines_n = data.readlines()
        new_text=''
        for i in data_lines_n :
            car_index = i.find('misc')
            if (car_index==0 ):
                data_lines_n.pop(i)
            car_index = i.find('DontCare')
            if (car_index == 0):
                data_lines_n.pop(i)




            print(car_index)

        shutil.copy(src_img, dst_img)
