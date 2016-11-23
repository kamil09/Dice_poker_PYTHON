import cv2
import numpy as np
from skimage.exposure import exposure

minSquare = 40

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

def passing(x):
    pass

# track = "Image"
# cv2.namedWindow(track)
# cv2.createTrackbar("c1", track, 80, 255, passing)
# cv2.createTrackbar("c2", track, 80, 255, passing)

def findAndDraw(image):
    if image is None: return
    img = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2HSV)

    img = cv2.medianBlur(img,5)
    innerRange= cv2.inRange(img, np.array([0, 0, 0],dtype="uint8"), np.array([10, 255, 255],dtype="uint8"))
    outerRange = cv2.inRange(img, np.array([160, 0, 0],dtype="uint8"), np.array([180, 255, 255],dtype="uint8"))
    wholeRange = innerRange + outerRange

    kernel = np.ones((3, 3), np.uint8)
    wholeRange = cv2.morphologyEx(wholeRange, cv2.MORPH_OPEN, kernel, iterations=2)
    wholeRange = cv2.morphologyEx(wholeRange,cv2.MORPH_CLOSE,kernel,iterations=2)

    img = cv2.bitwise_and(img,img,mask=wholeRange)
    test = img.copy()
    test = cv2.cvtColor(test, cv2.COLOR_HSV2BGR);

    # per = cv2.getTrackbarPos("c1",track)
    # per= np.percentile(img,v)    #RESCALE CONTRAST

    per = 80
    img[:,:,2] = exposure.rescale_intensity(img[:,:,2], in_range=(per, 150), out_range=(0, 255))


    # per = cv2.getTrackbarPos("c2",track)
    per = 10
    # per= np.percentile(img,s)    #RESCALE CONTRAST
    img[:,:,1] = exposure.rescale_intensity(img[:,:,1], in_range=(0, per), out_range=(0, 255))


    img[:,:,2] = img[:,:,2]*(((np.float32(img[:,:,1])/255)+1)/2)
    # img[:,:,1] = np.where(img[:,:,1] < 80, 0, 255)  # Expected results


    img = cv2.cvtColor(img,cv2.COLOR_HSV2BGR);
    imgR = img.copy()
    imgR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

    imgR = exposure.rescale_intensity(imgR, in_range=(0, 80), out_range=(0, 255))

    cv2.imshow("BEFORE", imgR)

    per, per2 = np.percentile(imgR,(80,100))    #RESCALE CONTRAST
    if per2 > per:
        imgR = exposure.rescale_intensity(imgR, in_range=(per,per2), out_range=(0,255))
    imgR = cv2.bilateralFilter(imgR, 10, 150, 150)  # Blur image, remove noise but keep edges
    ret, imgR = cv2.threshold(imgR, 120, 255, cv2.THRESH_BINARY)

    cv2.imshow("AFTER",imgR)
    dices = findSquares(imgR)
    if (dices is not None):
        for d in dices:
            # circles = findCircles2(img, d)
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
