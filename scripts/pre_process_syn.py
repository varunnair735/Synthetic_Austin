'''
@Author: Fanjie Kong
Create on 03/20/2019

Binarizing the synthetic label
    1. Truncate them to square
    2. Resize all the synthetic images to a fixed size
    3. Rename all the files and make sure that they are compatible to Bohao's code

'''

import glob, os
import scipy.misc as smc
import numpy as np
import re

final_res = (572, 572)
file_name_list = []
file_path = '/Users/Varun/Documents/CityEngine/Default Workspace/c3/images/austin2.7/raw/'


def num_2_str(num):
    num_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26']
    c_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    num2c = dict(zip(num_list, c_list))
    return ''.join([num2c[e_n] for e_n in num])


for file in glob.glob(file_path + "*RGB.jpg"):
    img = smc.imread(file)
    img_gt = smc.imread(file.replace('RGB', 'GT'))
    t_shape = min(img.shape[0], img.shape[1])

    img_GT = np.zeros((t_shape, t_shape))
    img_RGB = np.zeros((t_shape, t_shape, img.shape[2]))

    file = file.replace(file_path, '')
    # find the number in the name of file
    num = re.findall(r"\d+\.?\d*", file)

    print("-"*10+'Now processing '+ file +'-'*10)

    img_gt = img_gt[:t_shape, :t_shape, :]
    # Binarization
    for i in range(t_shape):
        for j in range(t_shape):
            img_GT[i, j] = 255 if (img_gt[i, j, 0], img_gt[i, j, 1], img_gt[i, j, 2]) < (35, 35, 35) else 0
    img_GT = smc.imresize(img_GT, final_res, interp='nearest')

    img_RGB = img[:t_shape, :t_shape, :]
    img_RGB = smc.imresize(img_RGB, final_res, interp='bilinear')

    # Eliminate redundancy (no-building patches)
    build_detector = np.sum(img_GT)
    if build_detector < 25500:
        print('No building in this patch!')
        continue
    else:
        smc.imsave('Austin' + '_' + num_2_str(num[0]) + '_' + num[1] + '_RGB.jpg'
                   , img_RGB)
        smc.imsave('Austin'+'_' + num_2_str(num[0])+'_' + num[1] + '_GT.jpg'
                   , img_GT)
    file_name_list.append('Austin' + '_' + num_2_str(num[0]) + '_' + num[1])

# save as file for collection
print(file_name_list)
np.savetxt('colTileNames.txt', np.array(file_name_list), fmt='%s', delimiter='\n')
