# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 10:56:19 2021

@author: Bryan Van Scoy
"""

import cv2 as cv
import numpy as np

filename = 'chessboard.png'
img = cv.imread(filename)
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

gray = np.float32(gray)
dst = cv.cornerHarris(gray,2,3,0.04)

# threshold
img[dst>0.01*dst.max()]=[0,0,255]

cv.imshow('dst',img)
cv.waitKey(0)
cv.destroyAllWindows()