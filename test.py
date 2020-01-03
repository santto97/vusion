from joblib import Parallel, delayed
from skimage import io, color
import csv
import cv2
import matplotlib.pyplot as plt
import multiprocessing
import numpy as np
import os


mascara = cv2.imread("5/13_850nm.png")
mascara = cv2.cvtColor(mascara, cv2.COLOR_BGR2RGB)

img = cv2.imread("5/6_590nm.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

imgYMax = -1
imgYMin = -1
imgXMax = -1
imgXMin = 640

for i in range(len(mascara)):
    for j in range(len(mascara[i])):
        if (mascara[i][j][0]**2+mascara[i][j][1]**2+mascara[i][j][2]**2)**0.5 >= 128:
            mascara[i][j][0] = img[i][j][0]
            mascara[i][j][1] = img[i][j][1]
            mascara[i][j][2] = img[i][j][2]

            if j > 10:

                if imgYMax == -1:
                    imgYMax = i
                imgYMin = i

                if imgXMin > j:
                    imgXMin = j                 

                if j > imgXMax:
                    imgXMax = j

        else:
            mascara[i][j][0] = 0
            mascara[i][j][1] = 0
            mascara[i][j][2] = 0


y = len(img)
x = len(img[1])
avg = np.zeros((y,x,3),dtype=int)
avg_color = img.mean(axis=0).mean(axis=0)


#for i in range(y):
#    for j in range(x):
#        avg[i][j][0]=round(avg_color[0])
#        avg[i][j][1]=round(avg_color[1])
#        avg[i][j][2]=round(avg_color[2])
#for i in range(y):
#    for j in range(x):
#        aux1 = (img[i][j][0]**2+img[i][j][1]**2+img[i][j][2]**2)**0.5
#        
#        if aux1*0.65 >= (avg[i][j][0]**2+avg[i][j][1]**2+avg[i][j][2]**2)**0.5:
#            img[i][j][0] = 255
#            img[i][j][1] = 0
#            img[i][j][2] = 0

print(imgYMax)
print(imgYMin)
print(imgXMax)
print(imgXMin)
        
plt.imshow(mascara)
plt.show()
