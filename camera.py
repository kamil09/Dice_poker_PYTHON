import cv2
import numpy as np
from skimage.exposure import exposure

def passing(x): pass
minSquare = 10

def findCircles(image, contours):   #RETURN LIST OF CIRCLES
    X = contours[:,0][:,0]
    Y = contours[:,0][:,1]
    if( max(X)-min(X)<minSquare or max(Y)-min(Y)<minSquare ): return []
    img = image[min(Y):max(Y),min(X):max(X)]
    img = exposure.rescale_intensity(img, in_range=(np.percentile(img, (50)), 255), out_range=(0, 255))
    size = max(max(X)-min(X) , max(Y)-min(Y))
    cv2.imshow("MAła kostka", img)

    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1000,1000)
    print(circles) #SHOULD PRINT CIRCLES :/
    if circles is None: return []
    circles = np.uint16(np.around(circles))
    return circles[0,:]

def findSquares(image):
    image2, conturs, hierarchy = cv2.findContours(image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    diceContours = []
    for c in conturs:
        perimeter = cv2.arcLength(c, True)
        approximation = cv2.approxPolyDP(c, 0.08 * perimeter, True)
        if len(approximation) == 4:
            diceContours.append(approximation)
    return diceContours

def findAndDraw(image):
    if image is None: return
    img = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
    imgR = image.copy()

    per, per2 = np.percentile(img, (80, 100))  # RESCALE CONTRAST
    img = exposure.rescale_intensity(img, in_range=(per, per2), out_range=(0, 255))

    imgR[:,:,0] = 0
    imgR[:,:,1] = 0
    imgR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

    per, per2 = np.percentile(imgR,(80,100))    #RESCALE CONTRAST
    imgR = exposure.rescale_intensity(imgR, in_range=(per,per2), out_range=(0,255))
    imgR = cv2.bilateralFilter(imgR, 10, 150, 150)  # Blur image, remove noise but keep edges
    ret, imgR = cv2.threshold(imgR, 120, 255, cv2.THRESH_BINARY)

    dices = findSquares(imgR)
    if (dices is not None):
        for d in dices:
            circles = findCircles(img, d)
            #for c in circles:
                #TODO DRAW CIRCLES
            cv2.drawContours(image, [d], -1, (0, 0, 255), 3)
    cv2.imshow("Kostki", image)

def playCamera(camera):
    cap, check = cv2.VideoCapture(camera), True
    while (check):
        check, klatka = cap.read()
        findAndDraw(klatka)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    playCamera(0)
