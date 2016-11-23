import cv2
import numpy as np
from skimage.exposure import exposure
import blob

def autoCanny(image,sigma=0.33):
    med = np.median(image)
    dolny = int(max(0,(1.0 - sigma)*med))
    gorny = int(min(255, (1.0 + sigma) * med))
    edges = cv2.Canny(image,dolny,gorny)
    return edges

minSquare = 40

def findCircles2(image):
    circles = cv2.HoughCircles(image,cv2.HOUGH_GRADIENT,1,40,param1=50,param2=30,minRadius=0,maxRadius=0)
    image = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
    if circles is None:
        return []
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2) #Outter circle
        cv2.circle(image,(i[0],i[1]),2,(255,0,0),3) #Center of a circle
    return image


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
        approximation = cv2.approxPolyDP(c, 0.1 * perimeter, True)
        if len(approximation) == 4:
            diceContours.append(approximation)
    return diceContours


def getRect(contour):
    pts = contour.reshape(4, 2)
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

def watershedAlgorythm(image,thresh):
    img = image.copy()
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    sure_bg = cv2.dilate(opening,kernel,iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    # Finding unknown region

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    markers = cv2.watershed(img, markers)
    # print(markers)
    markers = markers * -1
    markers = (markers +1)/2
    markers = markers * 255
    markers = np.uint8(markers)
    markers = cv2.bilateralFilter(markers, 10, 150, 150)  # Blur image, remove noise but keep edges

    # markers = cv2.GaussianBlur(markers,(5,5),0.2)
    # print(markers)
    img[markers != 0] = [255, 255, 255]
    img[markers == 0] = [0,0,0]

    return img

def findBlobs(image):
    detector = cv2.SimpleBlobDetector_create(blob.__blobSettings__)
    keypoints = detector.detect(image)
    return keypoints

def findAndDraw(image):
    if image is None:
        return
    img = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2HSV)

    img = cv2.medianBlur(img, 5)
    innerRange = cv2.inRange(img, np.array([0, 0, 0], dtype="uint8"), np.array([10, 255, 255], dtype="uint8"))
    outerRange = cv2.inRange(img, np.array([160, 0, 0], dtype="uint8"), np.array([180, 255, 255], dtype="uint8"))
    wholeRange = innerRange + outerRange

    kernel = np.ones((3, 3), np.uint8)
    wholeRange = cv2.morphologyEx(wholeRange, cv2.MORPH_OPEN, kernel, iterations=2)
    wholeRange = cv2.morphologyEx(wholeRange, cv2.MORPH_CLOSE, kernel, iterations=2)

    img = cv2.bitwise_and(img, img, mask=wholeRange)

    per = 90
    img[:, :, 2] = exposure.rescale_intensity(img[:, :, 2], in_range=(per, 180), out_range=(0, 255))

    # per = cv2.getTrackbarPos("c2",track)
    per = 10
    # per= np.percentile(img,s)    #RESCALE CONTRAST
    test = cv2.cvtColor(img,cv2.COLOR_HSV2BGR)
    # img[:, :, 1] = exposure.rescale_intensity(img[:, :, 1], in_range=(0, per), out_range=(0, 255))

    img[:, :, 2] = img[:, :, 2] * (((np.float32(img[:, :, 1]) / 255) + 1) / 2)
    # img[:,:,1] = np.where(img[:,:,1] < 80, 0, 255)  # Expected results


    test2 = cv2.cvtColor(img,cv2.COLOR_HSV2BGR)
    cv2.imshow("AFTER", np.hstack([test,test2]))
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR);
    imgR = img.copy()
    imgR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)

    imgR = exposure.rescale_intensity(imgR, in_range=(0, 80), out_range=(0, 255))


    per, per2 = np.percentile(imgR, (80, 100))  # RESCALE CONTRAST
    if per2 > per:
        imgR = exposure.rescale_intensity(imgR, in_range=(per, per2), out_range=(0, 255))
    imgR = cv2.bilateralFilter(imgR, 10, 150, 150)  # Blur image, remove noise but keep edges
    ret, imgR = cv2.threshold(imgR, 120, 255, cv2.THRESH_BINARY)

    imgR = cv2.morphologyEx(imgR, cv2.MORPH_CLOSE, kernel, iterations=4)
    imgR = cv2.morphologyEx(imgR, cv2.MORPH_OPEN, kernel, iterations=4)

    checkContour = watershedAlgorythm(image,imgR)
    checkContour = cv2.cvtColor(checkContour,cv2.COLOR_BGR2GRAY)
    #imgR = cv2.bitwise_and(imgR, imgR, mask=checkContour)
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
            if not (maxX - minX < minSquare or maxY - minY < minSquare):

                dice = perspectiveView(image.copy(),getRect(d))
                dice = cv2.resize(dice, None, fx=6, fy=6, interpolation=cv2.INTER_CUBIC)
                dice = cv2.cvtColor(dice,cv2.COLOR_BGR2GRAY)
                dice = 255 - dice
                dice = exposure.rescale_intensity(dice, in_range=(80, 140), out_range=(0, 255))
                keyPoints = findBlobs(dice)
                dice = cv2.cvtColor(dice,cv2.COLOR_GRAY2BGR)
                dice = cv2.drawKeypoints(dice,keyPoints,np.array([]),(0,255,0))
                if ( 0 < len(keyPoints) < 7):
                    kostki.append(len(keyPoints))
                cv2.imshow("Dice",dice)

                cv2.drawContours(image, [d], -1, (0, 0, 255), 3)
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
    for i in range(23):
        image = cv2.imread("images/"+str(i)+".jpg")
        _ = findAndDraw(image)
        while(True):
            if cv2.waitKey(1) & 0xFF == ord('q'): break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    # playCamera(0)
    checkImages()