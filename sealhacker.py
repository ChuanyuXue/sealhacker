#coding:utf-8
import cv2
import numpy as np
import os
from tqdm import tqdm


def process(impng, H_high, S_low):
    hue_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    low_range = np.array([130, 43, 46])
    high_range = np.array([180, 255, 255])
    th = cv2.inRange(hue_image, low_range, high_range)
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    th = cv2.dilate(th, element)
    index1 = th == 255
    img1 = np.zeros(impng.shape, np.uint8)
    img1[:,:,:] = (255, 255, 255, 0)
    img1[index1] = impng[index1]

    low_range = np.array([0, S_low, 46])
    high_range = np.array([H_high, 255, 255])
    th = cv2.inRange(hue_image, low_range, high_range)
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    th = cv2.dilate(th, element)
    index1 = th == 255
    img2 = np.zeros(impng.shape, np.uint8)
    img2[:,:,:] = (255, 255, 255, 0)
    img2[index1] = impng[index1]

    imgreal=cv2.add(img2, img1)

    white_px = np.asarray([255, 255, 255,255])

    (row, col, _) = imgreal.shape
    for r in range(row):
        for c in range(col):
            px = imgreal[r][c]
            if all(px == white_px):
                imgreal[r][c] = impng[r][c]

    #扩充图片防止截取部分
    img4png=cv2.copyMakeBorder(imgreal, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=[255, 255, 255,0])
    img2gray = cv2.cvtColor(img4png, cv2.COLOR_RGBA2GRAY)
    retval, grayfirst = cv2.threshold(img2gray, 254, 255, cv2.THRESH_BINARY_INV)

    # 再次膨胀，轮廓查找
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (22, 22))
    img6 = cv2.dilate(grayfirst, element)

    c_canny_img = cv2.Canny(img6, 10, 10)

    contours, hierarchy = cv2.findContours(c_canny_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    areas = []
    for i, cnt in enumerate(contours):
        rect = cv2.minAreaRect(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        ars = [area, i]
        areas.append(ars)
    areas = sorted(areas, reverse=True)
    maxares = areas[:1]

    x, y, w, h = cv2.boundingRect(contours[maxares[0][1]])
    temp = img4png[y:(y + h), x:(x + w)]

    cv2.imwrite('./output/out_%d_%d.png'%(H_high, S_low), temp)

import sys
 
if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        raise AssertionError('Must indicate the path of input file.')

    #加载图片
    print(input_path)
    image = cv2.imread(input_path)

    #统一处理图片大小
    img_w = 650 if image.shape[1] > 600 else 400
    image = cv2.resize(image, (img_w, int(img_w*image.shape[0]/image.shape[1])), interpolation=cv2.IMREAD_COLOR)
    impng=cv2.cvtColor(image.copy(), cv2.COLOR_RGB2RGBA)

    if not os.path.isdir('output'):
        os.mkdir('output')

    for H_high in tqdm([5,10,15,20,25,30,40,50]):
        for S_low in [10,20,30,40,50]:
            process(impng, H_high, S_low)
