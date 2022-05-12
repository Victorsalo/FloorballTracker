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

if sys.argv[1] == "":
    startnumber = 0
else:
    startnumber = sys.argv[1]
if sys.argv[2] == "":
    endnumber = 9
else:
    endnumber = sys.argv[2]
if sys.argv[3] == "":
    numberofimages = 10
else:
    numberofimages =sys.argv[3]

def most_frequent(List):
    t = [0] * len(List)
    for i in range(len(List)):
        for j in range(len(List)):
            if numpy.array_equal(List[i], List[j]):
                t[i] = t[i] +1
    t.index(max(t))
    return t.index(max(t))

def boundingbox(img, colorb, rader, columner):
    flag = False
    xmin = 101
    while xmin == 101:
        for i in range(columner):
            for j in range(rader):
                if numpy.array_equal(img[j, i], colorb) != True:
                    flag = True
                    xmin = i
                    break
            if flag == True:
                break
    flag = False
    ymin = 101
    while ymin == 101:
        for i in range(rader):
            for j in range(columner):
                if numpy.array_equal(img[i, j], colorb) != True:
                    flag = True
                    ymin = i
                    break
            if flag == True:
                break
    flag = False
    xmax = 101
    while xmax == 101:
        for i in range(columner):
            for j in range(rader):
                if numpy.array_equal(img[j, columner - 1 -i], colorb) != True:
                    flag = True
                    xmax = columner - i
                    break
            if flag == True:
                break
    flag = False
    ymax = 101
    while ymax == 101:
        for i in range(rader):
            for j in range(columner):
                if numpy.array_equal(img[rader -1 - i, j], colorb) != True:
                    flag = True
                    ymax = rader - i
                    break
            if flag == True:
                break
    x1 = (xmax + xmin) / (columner * 2)
    y1 = (ymax + ymin) / (rader * 2)
    x2 = (xmax - xmin) / columner
    y2 = (ymax - ymin) / rader
    return x1, y1, x2, y2

def imagedistort(img, arguments):
    img.distort('perspective', arguments)
    img = np.array(img)
    return img

def createimage(w, h, playernumber, color):
    colorlist = [(255, 0, 0),(255, 0, 255),(0, 255, 0),(0, 0, 204), (0, 0, 0), (255, 255, 255), (51, 255, 255)]
    n = color
    image_height = h
    image_width = w
    number_of_color_channels = 3
    color = colorlist[n]
    textx = random.randint(0, 40)
    texty = random.randint(33, 100)
    p = n
    while n == p:
        p = random.randint(0, len(colorlist) - 1)
    if playernumber < 10:
        pixel_array = numpy.full((image_height, image_width, number_of_color_channels), color, dtype=numpy.uint8)
        cv2.putText(img=pixel_array, text=str(playernumber), org=(textx, texty), fontFace=random.randint(0, 7), fontScale=1.5,
                color=colorlist[p], thickness=5)
        img = wi.from_array(pixel_array)
        angle = random.randint(-30, 30)
        img.distort('scale_rotate_translate', (angle,))
        parameter = 40
        dst1x = random.randint(0, parameter)
        dst1y = random.randint(0, parameter)
        dst2x = random.randint(100 - parameter, 100)
        dst2y = random.randint(0, parameter)
        dst3x = random.randint(0, parameter)
        dst3y = random.randint(100 - parameter, 100)
        dst4x = random.randint(100 - parameter, 100)
        dst4y = random.randint(100 - parameter, 100)
        arguments = (0, 0, dst1x, dst1y,
                     100, 0, dst2x, dst2y,
                     0, 100, dst3x, dst3y,
                     100, 100, dst4x, dst4y)
        img1  = imagedistort(img, arguments)
        img1 = np.array(img1)
        colorincorners = [img1[1, 1], img1[1, 99], img1[99, 1], img1[99, 99]]
        colorb = colorincorners[most_frequent(colorincorners)]
        x11, y11, x21, y21 = boundingbox(img1, colorb, 100, 100)
        senumber = img1
        x12 = 1
        y12 = 1
        x22 =1
        y22 = 1
        x13 = 1
        y13 = 1
        x23 = 1
        y23 = 1
    else:
        playernumber1 = playernumber // 10
        pixel_array1 = numpy.full((50, 40, number_of_color_channels), color, dtype=numpy.uint8)
        cv2.putText(img=pixel_array1, text=str(playernumber1), org=(5, 40), fontFace=random.randint(0, 7), fontScale=1.5,
                    color=colorlist[p], thickness=5)
        img1 = wi.from_array(pixel_array1)
        angle = random.randint(-30, 30)
        img1.distort('scale_rotate_translate', (angle,))
        firstnumber = numpy.full((100, 100, number_of_color_channels), color, dtype=numpy.uint8)
        firstnumber = wi.from_array(firstnumber)
        a = random.randint(0, 20)
        b = random.randint(10, 40)
        firstnumber.composite(img1, a, b)
        parameter = 40
        dst1x = random.randint(0, parameter)
        dst1y = random.randint(0, parameter)
        dst2x = random.randint(100 - parameter, 100)
        dst2y = random.randint(0, parameter)
        dst3x = random.randint(0, parameter)
        dst3y = random.randint(100 - parameter, 100)
        dst4x = random.randint(100 - parameter, 100)
        dst4y = random.randint(100 - parameter, 100)
        arguments = (0, 0, dst1x, dst1y,
                     100, 0, dst2x, dst2y,
                     0, 100, dst3x, dst3y,
                     100, 100, dst4x, dst4y)
        img1  = imagedistort(firstnumber, arguments)
        img1 = np.array(img1)
        colorincorners = [img1[1, 1], img1[1, 99], img1[99, 1], img1[99, 99]]
        colorb = colorincorners[most_frequent(colorincorners)]
        x11, y11, x21, y21 = boundingbox(img1, colorb, 100, 100)
        playernumber2 = playernumber - playernumber1*10
        pixel_array2 = numpy.full((50, 40, number_of_color_channels), color, dtype=numpy.uint8)
        cv2.putText(img=pixel_array2, text=str(playernumber2), org=(5, 40), fontFace=random.randint(0, 7), fontScale=1.5,
                    color=colorlist[p], thickness=5)
        img2 = wi.from_array(pixel_array2)
        angle = random.randint(-30, 30)
        img2.distort('scale_rotate_translate', (angle,))
        senumber = numpy.full((100, 100, number_of_color_channels), color, dtype=numpy.uint8)
        senumber = wi.from_array(senumber)
        a = a + random.randint(35, 45)
        b = b + random.randint(-10, 10)
        senumber.composite(img2, a, b)
        senumber = imagedistort(senumber, arguments)
        senumber = np.array(senumber)
        x12, y12, x22, y22 = boundingbox(senumber, colorb, 100, 100)
        firstnumber = np.array(firstnumber)
        for i in range(100):
            for j in range(100):
                if (senumber[i, j][0] == colorb[0]) and (senumber[i, j][1] == colorb[1]) and (senumber[i, j][2] == colorb[2]):
                    senumber[i, j] = firstnumber[i, j]
        x13 = (max(x11 + x21 / 2, x12 + x22 / 2) + min(x11 - x21 / 2, x12 - x22 / 2)) / 2
        y13 = (max(y11 + y21 / 2, y12 + y22 / 2) + min(y11 - y21 / 2, y12 - y22 / 2)) / 2
        x23 = max(x11 + x21 / 2, x12 + x22 / 2) - min(x11 - x21 / 2, x12 - x22 / 2)
        y23 = max(y11 + y21 / 2, y12 + y22 / 2) - min(y11 - y21 / 2, y12 - y22 / 2)
        colortxt = colorlist[p]
        colorincorners = [senumber[1, 1], senumber[1, 99], senumber[99, 1], senumber[99, 99]]
        colorb = colorincorners[most_frequent(colorincorners)]
    colortxt = colorlist[p]
    return senumber, colortxt, colorb , x11, y11, x21, y21, x12, y12, x22, y22, x13, y13, x23, y23



def imagetoimage(imagel, images):
    heightl, widthl, _ = imagel.shape
    heights, widths, _ = images.shape
    w = widthl - widths
    h = heightl - heights
    n = random.randint(0, w)
    m = random.randint(0, h)
    for i in range(heights):
        for j in range(widths):
            if (images[i, j][0] != 189) and (images[i, j][1] != 189) and (images[i, j][2] != 189):
                imagel[m + i, n + j] = images[i, j]
    return imagel


def writetotxt(filename, numberonplayer, x11, y11, x21, y21, x12, y12, x22, y22, x13, y13, x23, y23):
    f = open(str(filename) + ".txt", "w+")
    if numberonplayer >= 10:
        f.write(str(numberonplayer // 10) + ' ' + str(x11) + ' ' + str(y11) + ' ' + str(x21) + ' ' + str(y21) + '\n')
        f.write(str(numberonplayer - (numberonplayer // 10) * 10) + ' ' + str(x12) + ' ' + str(y12) + ' ' + str(x22) + ' ' + str(y22) + '\n')
    else:
        f.write(str(numberonplayer) + ' ' + str(x11) + ' ' + str(y11) + ' ' + str(x21) + ' ' + str(y21))
    f.close()


def writetoyaml(location, numbersofnumber):
    f = open(str(location) + '/' + 'data.yaml', 'w+')
    f.write('train: ' + location + '/images/train\n' + '\n')
    f.write('val: ' + location +  '/images/val\n' + '\n')
    f.write('test: ' + location + '/images/test\n' + '\n')
    f.write('nc: ' + str(numbersofnumber) + '\n')
    st = ''
    for i in range(numbersofnumber):
        if i == 0:
            st = """'""" + str(i) + """'"""
        else:
            st = st + ', ' + """'""" + str(i) + """'"""
    f.write('names: [' + st + ']')
starttime = time.time()
def simple2d(startnumber, endnumber, numberofimages):
    t = 0
    folder = 'data'
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
        writetoyaml(folder , 10)
    for playernumber in range(100):
        starttimenumber = time.time()
        playernumbers = playernumber
        #os.mkdir('simdata/' + str(playernumbers))
        for color in range(7):
            for k in range(int(numberofimages)):
                t = t + 1
                if int(startnumber) <= int(playernumbers) <= int(endnumber):
                    numberatedge = True
                    while numberatedge:
                        img, colortxt, colorb, x11, y11, x21, y21, x12, y12, x22, y22, x13, y13, x23, y23 = createimage(100, 100, playernumbers, color)
                        tt = 0
                        for i in range(100):
                            if numpy.array_equal(img[i, 0], colorb) and numpy.array_equal(img[i, 99], colorb) and numpy.array_equal(img[99, i], colorb) and numpy.array_equal(img[0, i], colorb):
                                tt = tt + 1
                        if tt == 100:
                            numberatedge = False
                    num_str = repr(t - 1)
                    last_digit_str = num_str[-1]
                    last_digit = int(last_digit_str)
                    if last_digit <=7:
                        cv2.imwrite(folder + '/images/train/' + str(t) + '.jpg', img)
                        writetotxt(folder + '/labels/train/' + str(t), playernumbers, x11, y11, x21, y21, x12, y12, x22, y22, x13, y13, x23, y23)
                    elif last_digit == 8:
                        cv2.imwrite(folder + '/images/val/' + str(t) + '.jpg', img)
                        writetotxt(folder + '/labels/val/' + str(t), playernumbers, x11, y11, x21, y21, x12, y12, x22,
                                   y22, x13, y13, x23, y23)
                    else:
                        cv2.imwrite(folder + '/images/test/' + str(t) + '.jpg', img)
                        writetotxt(folder + '/labels/test/' + str(t), playernumbers, x11, y11, x21, y21, x12, y12, x22,
                                   y22, x13, y13, x23, y23)
        print(str(playernumbers) + ' ' + str(time.time() - starttimenumber) + ' ' + str(time.time() - starttime))
print(time.time() - starttime)