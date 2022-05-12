import sys
import numpy as np
# from PIL import Image
import cv2
import numpy
import random
import time
import os
import operator
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
from wand.image import Image as wi

def writetotxt(filename, numberonplayer, x11, y11, x21, y21, x12, y12, x22, y22, x13, y13, x23, y23):
    f = open(str(filename) + ".txt", "w+")
    if numberonplayer >= 10:
        f.write(str(numberonplayer // 10) + ' ' + str(x11) + ' ' + str(y11) + ' ' + str(x21) + ' ' + str(y21) + '\n')
        f.write(str(numberonplayer - (numberonplayer // 10) * 10) + ' ' + str(x12) + ' ' + str(y12) + ' ' + str(x22) + ' ' + str(y22) + '\n')
        #f.write(str(numberonplayer) + ' ' + str(x13) + ' ' + str(y13) + ' ' + str(x23) + ' ' + str(y23))
    else:
        f.write(str(numberonplayer) + ' ' + str(x11) + ' ' + str(y11) + ' ' + str(x21) + ' ' + str(y21))
    f.close()

def writetoyaml(location, numbersofnumber):
    f = open(str(location) + '/' + 'datacomplex.yaml', 'w+')
    f.write('train: ' + location + '/images/train\n' + '\n')
    f.write('val: ' + location +  '/images/val\n' + '\n')
    f.write('test: ' + location + '/images/test\n' + '\n')
    # val:../ valid / images

    f.write('nc: ' + str(numbersofnumber) + '\n')
    st = ''
    for i in range(numbersofnumber):
        if i == 0:
            st = """'""" + str(i) + """'"""
        else:
            st = st + ', ' + """'""" + str(i) + """'"""
    f.write('names: [' + st + ']')

def imagetoimage(imagel, images):
    heightl, widthl, _ = imagel.shape
    heights, widths, _ = images.shape
    w = widthl - widths
    h = heightl - heights
    n = random.randint(0, w)
    m = random.randint(0, h)
    for i in range(heights):
        for j in range(widths):

            imagel[m + i, n + j] = images[i, j]

    return imagel, n, m

def rchop(s, suffix):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    return s

def complex2d():
    startnumber = 0
    t = 0
    numfiles = len(os.listdir('train2017'))
    folder = 'datacomplex'
    if int(startnumber) == 0:
        os.mkdir(folder)
        os.mkdir(folder + '/images')
        os.mkdir(folder + '/labels')
        os.mkdir(folder + '/labels/train')
        os.mkdir(folder + '/images/train')
        os.mkdir(folder + '/labels/val')
        os.mkdir(folder + '/images/val')
        os.mkdir(folder + '/labels/test')
        os.mkdir(folder + '/images/test')
        writetoyaml(folder, 10)
    for playernumber in range(100):

        for i in range(4000):
            t = t + 1

            # cocoimage = random.choice(os.listdir("train2017"))
            imagenumber = random.randint((playernumber * 700) + 1, ((playernumber + 1) * 700))
            simple2dimage = str(imagenumber) + '.jpg'
            # print(simple2dimage)
            cocoimage = str(random.randint(1, numfiles - 1))
            cocoimagecv = cv2.imread('train2017/' + cocoimage + '.jpg')
            # cocoimagecv = np.array(cocoimage)
            # simple2dimage = random.choice(os.listdir('simdirectory/' + str(playernumber)))
            # 1. Get the string representation
            num_str = repr(imagenumber)
            # 2. Access the last string of the digit string:
            last_digit_str = num_str[-1]
            # 3. Convert the last digit string to an integer:
            last_digit = int(last_digit_str)

            if last_digit <= 8 and last_digit != 0:
                simple2dimagecv = cv2.imread('data/images/train/' + simple2dimage)
            elif last_digit == 9:
                simple2dimagecv = cv2.imread('data/images/val/' + simple2dimage)
            else:
                simple2dimagecv = cv2.imread('data/images/test/' + simple2dimage)
            # simple2dimage = np.array(simple2dimage)
            imagel = cv2.resize(cocoimagecv, dsize=(100, 100), interpolation=cv2.INTER_CUBIC)

            images = cv2.resize(simple2dimagecv, dsize=(50, 50), interpolation=cv2.INTER_CUBIC)
            img, n, m = imagetoimage(imagel, images)

            if last_digit <= 8 and last_digit != 0:
                file1 = open('data/labels/train/' + str(imagenumber) + '.txt', 'r')
            elif last_digit == 9:
                file1 = open('data/labels/val/' + str(imagenumber) + '.txt', 'r')
            else:
                file1 = open('data/labels/test/' + str(imagenumber) + '.txt', 'r')

            lines = file1.readlines()
            if len(lines) == 2:
                object1 = lines[0].split(' ')

                object2 = lines[1].split(' ')
                playernumbers = int(object1[0] + object2[0])
                x11 = float(object1[1])/2 + n/100
                y11 = float(object1[2])/2 + m/100
                x21 = float(object1[3])/2
                y21 = float(rchop(object1[4], '\n')) /2
                x12 = float(object2[1])/2 + n/100
                y12 = float(object2[2])/2 + m/100
                x22 = float(object2[3])/2
                y22 = float(rchop(object2[4], '\n')) /2
                x13 = 1
                y13 = 1
                x23 = 1
                y23 = 1

            else:
                object1 = lines[0].split(' ')
                playernumbers = int(object1[0])
                x11 = float(object1[1])/2 + n/100
                y11 = float(object1[2])/2 + m/100
                x21 = float(object1[3])/2
                y21 = float(rchop(object1[4], '\n')) /2
                x12 = 1
                y12 = 1
                x22 = 1
                y22 = 1
                x13 = 1
                y13 = 1
                x23 = 1
                y23 = 1

            file1.close()

            if last_digit <= 8 and last_digit!= 0:
                cv2.imwrite(folder + '/images/train/' + str(t) + '.jpg', img)
                writetotxt(folder + '/labels/train/' + str(t), playernumbers, x11, y11, x21, y21, x12, y12, x22, y22,
                            x13, y13, x23, y23)
            elif last_digit == 9:
                cv2.imwrite(folder + '/images/val/' + str(t) + '.jpg', img)
                writetotxt(folder + '/labels/val/' + str(t), playernumbers, x11, y11, x21, y21, x12, y12, x22,
                            y22, x13, y13, x23, y23)
            else:
                cv2.imwrite(folder + '/images/test/' + str(t) + '.jpg', img)
                writetotxt(folder + '/labels/test/' + str(t), playernumbers, x11, y11, x21, y21, x12, y12, x22,
                            y22, x13, y13, x23, y23)

        print(playernumber)

starttime = time.time()
#complex2d()
print(time.time() - starttime)
cocoimagecv = cv2.imread('cocosub.jpg')
imagel = cv2.resize(cocoimagecv, dsize=(100, 100), interpolation=cv2.INTER_CUBIC)
simple2dimagecv = cv2.imread('yolov5/data/images/test/19840.jpg')
images = cv2.resize(simple2dimagecv, dsize=(50, 50), interpolation=cv2.INTER_CUBIC)
imagel,n,m = imagetoimage(imagel, images)
cv2.imwrite('tjenatjena.jpg', imagel)