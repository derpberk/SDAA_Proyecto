#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import time
import numpy as np

def nothing(x):
    pass

if __name__== "__main__":

    cv2.namedWindow('image')

    cv2.createTrackbar('Angulo acimutal','image',0,180,nothing)
    cv2.createTrackbar('Angulo longitudinal','image',0,180,nothing)

    while(1):

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

        # get current positions of four trackbars
        acimutal = cv2.getTrackbarPos('Angulo acimutal','image')
        longitudinal = cv2.getTrackbarPos('Angulo longitudinal','image')
        time.sleep(0.1)
        print("Angulo acimutal: " + str(acimutal) + " Angulo longitudinal: " + str(longitudinal))

    cv2.destroyAllWindows()
    exit(0)