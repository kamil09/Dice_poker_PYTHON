#USTAWIENIA DLA ZNAJDYWANIA OCZEK NA KOSTCE

import cv2

__blobSettings__ = cv2.SimpleBlobDetector_Params()

__blobSettings__.minThreshold = 0;
__blobSettings__.maxThreshold = 255;

__blobSettings__.filterByArea = True
__blobSettings__.minArea = 20*20*3.14

__blobSettings__.filterByCircularity = True
__blobSettings__.minCircularity = 0.5

__blobSettings__.filterByConvexity = True
__blobSettings__.minConvexity = 0.6

__blobSettings__.filterByInertia = True
__blobSettings__.minInertiaRatio = 0.01

