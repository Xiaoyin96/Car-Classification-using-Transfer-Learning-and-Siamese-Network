import os
import colorsys
import PIL.Image as Image
import cv2
import numpy as np
import colorList
import matplotlib.pyplot as plt
import pandas as pd
import csv

def get_color(frame, classFolder, imgName):
    #print('go in get_color')
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    color_dict = colorList.getColorList()
    for color in color_dict:
        mask = cv2.inRange(hsv,color_dict[color][0],color_dict[color][1])
        fileName = os.path.join(classFolder, color)
        cv2.imwrite(os.path.join(fileName, imgName[:-4]+'.jpg'),mask)

    return

    
def get_color_samefolder(frame, classFolder, imgName):
    #print('go in get_color')
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    color_dict = colorList.getColorList()
    for color in color_dict:
        mask = cv2.inRange(hsv,color_dict[color][0],color_dict[color][1])
        #fileName = os.path.join(classFolder, color)
        fileName = classFolder
        binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
        binary = cv2.dilate(binary,None,iterations=2)
        img, cnts, hiera = cv2.findContours(binary.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        sum = 0
        for c in cnts:
            sum+=cv2.contourArea(c)
        if sum >= 20000 :
            cv2.imwrite(os.path.join(fileName, imgName[:-4]+color+'.jpg'),mask)

    return    
    
def rgb_split(file):
    im = Image.open(file)
    r,g,b = im.split()
    ar = np.array(r).flatten() 
    nr, bins, patches = plt.hist(ar,bins = 256, density = 1)

    ag = np.array(g).flatten()
    ng, bins, patches = plt.hist(ag,bins = 256, density = 1)

    ab = np.array(b).flatten()
    nb, bins, patches = plt.hist(ab,bins = 256, density = 1)
    return (nr, ng, nb)
    
    
if __name__ == '__main__':
    
    filePath = '.\train_twin'
    savePathMaster = '.\train_twin_gray'
    
    color_dict = colorList.getColorList()
    for folders,dirc,files in os.walk(filePath):  
        # folders = filePath
        # dirc = dictionary
        # files = picture name
        className = os.path.split(folders)[-1]
        if className == 'train_twin':
            continue
        if className == 'test':
            continue
        if className == 'valid':
            continue
        savePath = os.path.join(savePathMaster,className)
        if not os.path.exists(savePath):
            os.makedirs(savePath)
            print('--- Make A New Folder')
        #for color in color_dict:
        #    colorPath = os.path.join(savePath,color)
        #    if not os.path.exists(colorPath):
        #        os.makedirs(colorPath)
                    
        distribution = np.zeros((len(files),256*3))


        for imgName in files:
            file = os.path.join(folders,imgName)
            
            frame = cv2.imread(file)
            
            get_color_samefolder(frame, savePath, imgName)

            print(imgName)

        print('--- Done with class ' + className + ' ---')
