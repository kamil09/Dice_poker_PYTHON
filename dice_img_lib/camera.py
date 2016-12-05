import cv2
import numpy as np
from skimage.exposure import exposure
from dice_img_lib import const as cst

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

    pts = sorted(pts,key=lambda x: x[0])
    # print(pts)
    if pts[-1][1] > pts[-2][1]:
        rect[1] = pts[-1]
        rect[2] = pts[-2]
    else:
        rect[1] = pts[-2]
        rect[2] = pts[-1]
    if pts[0][1] > pts[1][1]:
        rect[0] = pts[0]
        rect[3] = pts[1]
    else:
        rect[0] = pts[1]
        rect[3] = pts[0]
    return rect

def getLine(point1,point2):
    a = 0
    deltaX = point1[0] - point2[0]
    deltaY = point1[1] - point2[1]
    if deltaX == 0:
        # deltaX = 1
        a = deltaY
    elif deltaY == 0:
        a = deltaX
    else:
        a = deltaY/deltaX
    b = point2[1]
    c = point2[0]
    return a,b,c


def getMiddlePoint(rect):
    a1,b1,c1 = getLine(rect[2],rect[0])
    a2,b2,c2 = getLine(rect[3],rect[1])
    x = (c1*a1 - c2*a2 + b2 - b1)/(a1 - a2)
    y = a1*(x-c1) + b1
    point = []
    point.append(x)
    point.append(y)
    return point

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

    per1, per2 = np.percentile(img[:,:,0], (cst.rescaleH_per_min, cst.rescaleH_per_max))
    img[:,:,0] = exposure.rescale_intensity(img[:, :, 0], in_range=(per1, per2), out_range=(0, 180))
    per1, per2 = np.percentile(img[:, :, 1], (cst.rescaleS_per_min, cst.rescaleS_per_max))
    img[:, :, 1] = exposure.rescale_intensity(img[:, :, 1], in_range=(per1, per2), out_range=(0, 255))
    per1, per2 = np.percentile(img[:, :, 2], (cst.rescaleV_per_min, cst.rescaleV_per_max))
    img[:, :, 2] = exposure.rescale_intensity(img[:, :, 2], in_range=(per1, per2), out_range=(0, 255))

    img = cv2.medianBlur(img, cst.median_blur)
    perS = np.percentile(img[:,:,1], cst.progS_min)
    perV = np.percentile(img[:,:,2], cst.progV_min)
    innerRange = cv2.inRange(img,
                             np.array([cst.progH_min, perS, perV], dtype="uint8"),
                             np.array([cst.progH_max, cst.progS_max, cst.progV_max], dtype="uint8"))

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

    middlePoints = []
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
                rect = getRect(d)
                # print(rect)
                dice = perspectiveView(image.copy(),rect)
                middle = getMiddlePoint(rect)
                cv2.circle(image, (middle[0], middle[1]), 2, (255, 0, 0), 3)  # Center of a circle
                middlePoints.append(middle)

                dice = cv2.resize(dice, None, fx=400/size, fy=400/size, interpolation=cv2.INTER_CUBIC)

                dice = dice[:,:,1]
                dice = 255 - dice
                p = np.percentile(dice, 4)

                dice = exposure.rescale_intensity(dice, in_range=(p, 255), out_range=(0, 255))

                keyPoints = findBlobs(dice)
                dice = cv2.cvtColor(dice,cv2.COLOR_GRAY2BGR)
                dice = cv2.drawKeypoints(dice,keyPoints,np.array([]),(0,255,0))
                if ( 0 < len(keyPoints) < 7):
                    kostki.append(len(keyPoints))
                #cv2.imshow("Dice",dice)

                cv2.drawContours(image, [d], -1, (0, 0, 255), 3)

    image = cv2.resize(image, None, fx=800/image.shape[1], fy=600/image.shape[0], interpolation=cv2.INTER_CUBIC)
    cv2.imshow("Kostki", image)
    return kostki,middlePoints


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
        kostki,_ = findAndDraw(klatka)
        print(kostki)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cap.release()
    cv2.destroyAllWindows()

def checkImages():
    coverageMatrix = []
    allCorrect = 0
    allWrong = 0
    allMissed = 0
    for i in range(65):
        fileName = "../images/"+str(i+1)
        image = cv2.imread(fileName+".jpg")
        kostki,middlePoints = findAndDraw(image)
        print(kostki)
        test = cv2.imread(fileName+"test.png")
        correct,wrong,missed = checkRectangle(test,middlePoints)
        # print("Correct: " + str(correct))
        # print("Wrong: "+ str(wrong))
        # print("Missed: "+ str(missed))
        krotka = [correct,wrong,missed]
        coverageMatrix.append(krotka)
        allCorrect += correct
        allWrong += wrong
        allMissed += missed
        # while(True):
        #     if cv2.waitKey(1) & 0xFF == ord('q'): break
    # allCorrect = np.sum(coverageMatrix[:,0])
    # allWrong = np.sum(coverageMatrix[:,1])
    # allMissed = np.sum(coverageMatrix[:,2])
    print("All correct: " + str(allCorrect) + " ALL WRONG: " + str(allWrong) + " ALL MISSED: " + str(allMissed))
    result = (allCorrect-allWrong)/(allCorrect+allMissed)
    print(result)
    cv2.destroyAllWindows()

def checkRectangle(image,points):
    middlePoints = points
    dices = findSquares(cv2.cvtColor(image,cv2.COLOR_BGR2GRAY))
    correct = 0
    wrong = 0
    middleDices = []
    for d in dices:
        rect = getRect(d)
        middle = getMiddlePoint(rect)
        cv2.circle(image, (middle[0], middle[1]), 2, (255, 0, 0), 3)  # Center of a circle
        middleDices.append(middle)
        distance = np.sqrt(((rect[0][0] - middle[0])**2)+((rect[0][1] - middle[1])**2))
        distance = distance*0.8
        middleDices[-1].append(distance)
    for point in middlePoints:
        found = None
        for d in middleDices:
            distance = np.sqrt(((point[0] - d[0])**2)+((point[1]-d[1])**2))
            if distance < d[2]:
                cv2.circle(image, (d[0], d[1]), 2, (0, 255, 255), 3)  # Center of a circle
                found = d
                break
        if found is not None:
            correct = correct + 1
            middleDices.remove(found)
            cv2.circle(image, (point[0], point[1]), 2, (0, 255, 0), 3)  # Center of a circle
        else:
            wrong = wrong +1
            cv2.circle(image, (point[0], point[1]), 2, (0, 0, 255), 3)  # Center of a circle
    missed = len(middleDices)

    image = cv2.resize(image, None, fx=800 / image.shape[1], fy=600 / image.shape[0], interpolation=cv2.INTER_CUBIC)
    cv2.imshow("TEST",image)
    return correct,wrong,missed

if __name__ == '__main__':
    # playCamera(0)
    checkImages()
