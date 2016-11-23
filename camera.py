import cv2
import numpy as np
from skimage.exposure import exposure


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


def findAndDraw(image):
    if image is None: return
    img = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2HSV)

    img = cv2.medianBlur(img,5)
    innerRange= cv2.inRange(img, np.array([0, 0, 0],dtype="uint8"), np.array([10, 255, 255],dtype="uint8"))
    outerRange = cv2.inRange(img, np.array([170, 0, 0],dtype="uint8"), np.array([180, 255, 255],dtype="uint8"))
    wholeRange = innerRange + outerRange

    kernel = np.ones((3, 3), np.uint8)
    # wholeRange = cv2.morphologyEx(wholeRange, cv2.MORPH_OPEN, kernel, iterations=2)
    wholeRange = cv2.morphologyEx(wholeRange,cv2.MORPH_CLOSE,kernel,iterations=2)

    img = cv2.bitwise_and(img,img,mask=wholeRange)

    img = cv2.cvtColor(img,cv2.COLOR_HSV2BGR);
    cv2.imshow("before",img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);

    # ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_TOZERO)
    #
    # value = 50
    # img = np.where( ((255 - img) < value),255,img+value)

    # per, per2 = np.percentile(img, (80, 100))  # RESCALE CONTRAST
    # if per2 > per:
    #     img = exposure.rescale_intensity(img, in_range=(per, per2), out_range=(0, 255))

    img = cv2.equalizeHist(img)

    img = cv2.medianBlur(img, 5)
    kernel = np.ones((3,3),np.uint8)
    img = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel,iterations=2)

    distance = cv2.distanceTransform(img,2,3)
    cv2.normalize(distance,distance,0,1.2,cv2.NORM_MINMAX)


    dices = findSquares(img)
    edges = autoCanny(img)
    cv2.imshow("after",edges)

    if (dices is not None):
        for d in dices:
            X = d[:, 0][:, 0]
            Y = d[:, 0][:, 1]
            minX = min(X)
            maxX = max(X)
            minY = min(Y)
            maxY = max(Y)
            if not (maxX - minX < minSquare or maxY - minY < minSquare):
                cv2.imshow("KOSTKA",image[minY:maxY,minX:maxX])

                # dice = perspectiveView(image,getRect(d))
                # cv2.imshow("Dice",dice)

                # circles = findCircles(img, d)
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
