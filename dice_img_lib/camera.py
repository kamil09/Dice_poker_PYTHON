import cv2
import numpy as np
from skimage.exposure import exposure

from dice_img_lib import blob

minSquare = 40

def findSquares(image):
    image2, conturs, hierarchy = cv2.findContours(image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)

    diceContours = []
    for c in conturs:
        perimeter = cv2.arcLength(c, True)
        approximation = cv2.approxPolyDP(c, 0.1 * perimeter, True)
        if len(approximation) >= 4:
            diceContours.append(approximation)
    return diceContours


def getRect(contour):
    pts = contour.reshape(len(contour), 2)
    rect = np.zeros((4, 2), dtype="float32")

    suma = pts.sum(axis=1)
    rect[0] = pts[np.argmin(suma)]
    rect[2] = pts[np.argmax(suma)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def perspectiveView(image,rect):

    (topLeft,topRight,bottomRight,bottomLeft) = rect
    widthBottom = np.sqrt(((bottomRight[0] - bottomLeft[0]) ** 2) + ((bottomRight[1] - bottomLeft[1]) ** 2))
    widthTop = np.sqrt(((topRight[0] - topLeft[0]) ** 2) + ((topRight[1] - topLeft[1]) ** 2))

    maxWidth = max(widthBottom,widthTop)

    heightRight = np.sqrt(((topRight[0]-bottomRight[0]) ** 2) + ((topRight[1]- bottomRight[1]) ** 2))
    heightLeft = np.sqrt(((topLeft[0]-bottomLeft[0]) ** 2) + ((topLeft[1]-bottomLeft[1]) ** 2))

    maxHeight = max(heightRight,heightLeft)
    dst = np.array([
        [0,0],
        [maxWidth -1,0],
        [maxWidth-1,maxHeight-1],
        [0, maxHeight-1]],
        dtype = "float32")
    transform = cv2.getPerspectiveTransform(rect,dst)
    warp = cv2.warpPerspective(image,transform,(int(maxWidth),int(maxHeight)))
    return warp

def findBlobs(image):
    detector = cv2.SimpleBlobDetector_create(blob.__blobSettings__)
    keypoints = detector.detect(image)
    return keypoints

def findAndDraw(image):
    if image is None: return

    img = image.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    per1, per2 = np.percentile(img[:,:,0], (5, 50))
    img[:,:,0] = exposure.rescale_intensity(img[:, :, 0], in_range=(per1, per2), out_range=(0, 180))

    per1, per2 = np.percentile(img[:, :, 1], (5, 100))
    img[:, :, 1] = exposure.rescale_intensity(img[:, :, 1], in_range=(per1, per2), out_range=(0, 255))

    per1, per2 = np.percentile(img[:, :, 2], (6, 100))
    img[:, :, 2] = exposure.rescale_intensity(img[:, :, 2], in_range=(per1, per2), out_range=(0, 255))

    img = cv2.medianBlur(img, 5)

    innerRange = cv2.inRange(img, np.array([0, 50, 0], dtype="uint8"), np.array([25, 255, 255], dtype="uint8"))

    kernel = np.ones((6, 6), np.uint8)
    innerRange = cv2.morphologyEx(innerRange, cv2.MORPH_CLOSE, kernel, iterations=2)
    img[:,:,2] = cv2.bitwise_and(img[:,:,2], img[:,:,2], mask=innerRange)

    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    imgR = img.copy()
    imgR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

    imgR = cv2.bilateralFilter(imgR, 10, 150, 150)  # Blur image, remove noise but keep edges
    imgR = exposure.rescale_intensity(imgR, in_range=(0, 100), out_range=(0, 255))

    kernel = np.ones((3, 3), np.uint8)
    imgR = cv2.morphologyEx(imgR, cv2.MORPH_OPEN, kernel, iterations=6)

    dices = findSquares(imgR)

    kostki = []
    if (dices is not None):
        for d in dices:
            X = d[:, 0][:, 0]
            Y = d[:, 0][:, 1]
            minX = min(X)
            maxX = max(X)
            minY = min(Y)
            maxY = max(Y)
            size = max(maxY-minY, maxX-minX)
            if not (maxX - minX < minSquare or maxY - minY < minSquare):

                dice = perspectiveView(image.copy(),getRect(d))


                dice = cv2.resize(dice, None, fx=400/size, fy=400/size, interpolation=cv2.INTER_CUBIC)

                dice = dice[:,:,1]
                #dice = cv2.cvtColor(dice,cv2.COLOR_BGR2GRAY)
                dice = 255 - dice
                p = np.percentile(dice, 4)

                dice = exposure.rescale_intensity(dice, in_range=(p, 255), out_range=(0, 255))


                keyPoints = findBlobs(dice)
                dice = cv2.cvtColor(dice,cv2.COLOR_GRAY2BGR)
                dice = cv2.drawKeypoints(dice,keyPoints,np.array([]),(0,255,0))
                if ( 0 < len(keyPoints) < 7):
                    kostki.append(len(keyPoints))
                cv2.imshow("Dice",dice)

                cv2.drawContours(image, [d], -1, (0, 0, 255), 3)

    image = cv2.resize(image, None, fx=800/image.shape[1], fy=600/image.shape[0], interpolation=cv2.INTER_CUBIC)
    cv2.imshow("Kostki", image)
    return kostki


def probkowanie(tablicaKostek,kostki):
    kostki = sorted(kostki)

    tablicaKostek.append(kostki)
    return tablicaKostek

def playCamera(camera):
    cap, check = cv2.VideoCapture(camera), True
    cap.set(3,640)
    cap.set(4,480)
    while (check):
        check, klatka = cap.read()
        kostki = findAndDraw(klatka)
        print(kostki)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cap.release()
    cv2.destroyAllWindows()

def checkImages():
    for i in range(65):
        image = cv2.imread("images/"+str(i+1)+".jpg")
        kostki = findAndDraw(image)
        print(kostki)

        while(True):
            if cv2.waitKey(1) & 0xFF == ord('q'): break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    # playCamera(0)
    checkImages()
