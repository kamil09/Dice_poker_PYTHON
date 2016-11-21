import cv2
import numpy as np
from skimage import color,io
import matplotlib as mp
from skimage.restoration import denoise_bilateral

def passing(x):
    pass

def autoCanny(image,sigma=0.33):
    med = np.median(image)
    dolny = int(max(0,(1.0 - sigma)*med))
    gorny = int(min(255, (1.0 + sigma) * med))
    edges = cv2.Canny(image,dolny,gorny)
    return edges

# trackbars
track = "Image"
cv2.namedWindow(track)
cv2.createTrackbar("c1", track, 80, 255, passing)
# cv2.createTrackbar("c2", track, 10, 500, passing)
cv2.createTrackbar("c3", track, 10, 500, passing)
cv2.createTrackbar("c4", track, 10, 500, passing)
cv2.createTrackbar("c5", track, 10, 100, passing)
cv2.createTrackbar("c6", track, 1, 100, passing)
cv2.createTrackbar("c7", track, 10, 100, passing)


switch = '0 : OFF \n1 : ON'


def findCircles(image):
    circles = cv2.HoughCircles(image,cv2.HOUGH_GRADIENT,1,40,param1=50,param2=30,minRadius=0,maxRadius=0)
    # c6 = cv2.getTrackbarPos("c6",track)
    # c7 = cv2.getTrackbarPos("c7",track)
    # circles = cv2.HoughCircles(image,cv2.HOUGH_GRADIENT,c6,c7)
    image = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
    if circles is None:
        return image
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2) #Outter circle
        cv2.circle(image,(i[0],i[1]),2,(255,0,0),3) #Center of a circle
    return image

def findSquares(image):
    if image is None:
        return image
    image2, conturs, hierarchy = cv2.findContours(image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # conturs = sorted(conturs,key = cv2.contourArea,reverse = True)[:20]
    diceContours = []
    for c in conturs:
        perimeter = cv2.arcLength(c, True)
        aprox = cv2.getTrackbarPos("c5",track)/100.0
        approximation = cv2.approxPolyDP(c, aprox * perimeter, True)
        if len(approximation) == 4:
            diceContours.append(approximation)
    return diceContours

def findDice(image):
    # fgbg = cv2.createBackgroundSubtractorMOG2()

    # cv2.imshow('Real image',klatka)
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # kernel = np.ones((5,5),np.uint8)
    # grey = cv2.equalizeHist(grey)
    # grey = fgbg.apply(grey)
    # cv2.imshow("test",grey)
    # clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
    # grey = clahe.apply(grey)
    # grey = cv2.bilateralFilter(grey, 1, 20, 20)  # Blur image, remove noise but keep edges
    # edges = grey
    edges = cv2.Canny(grey, 10, 200)

    image2, conturs, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # conturs = sorted(conturs,key = cv2.contourArea,reverse = True)[:20]
    diceContours = []
    for c in conturs:
        perimeter = cv2.arcLength(c, True)
        #Nie wiem czy to jest ok.
        perimeter *=5
        aprox = 0.02
        approximation = cv2.approxPolyDP(c, aprox * perimeter, True)
        if len(approximation) == 4:
            diceContours.append(approximation)
        # diceContours.append(approximation)

    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    # circle = findCircles(edges)
    for d in diceContours:
        # print(d)
        # cv2.drawContours(circle, [d], -1, (0, 0, 255), 3)
        cv2.drawContours(edges, [d], -1, (0, 0, 255), 3)
    # cv2.imshow(track,circle)
    cv2.imshow(track,edges)




def testowanie(image):
    img = image
    # cv2.imshow("test",img)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # for i in range(len(img)):
    #     for j in range(len(img[i])):
    #         img[i][j][0] = int((img[i][j][0]/10))*10

    img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # min = cv2.getTrackbarPos("c1",track)
    # max = cv2.getTrackbarPos("c2", track)
    # min = 0
    # max = 30
    # redObjects = 0
    # np.array(redObjects)
    test1 = cv2.inRange(img,np.array([0,100,0]),np.array([20,255,255]))
    test2 = cv2.inRange(img,np.array([160,100,0]),np.array([180,255,255]))
    test = test1 + test2
    # print(test)
    # img[: ,: ,0] = img[:,:,0] * test[:,:]
    # img[:, :, 1] = img[:, :, 1] * test[:, :]
    img[:, :, 2] = img[:, :, 2] * test[:, :]

    img = cv2.cvtColor(img,cv2.COLOR_HSV2BGR)
    cv2.imshow("imageTest",img)
    # cv2.imshow("test",test1)
    # cv2.imshow("test2",test2)
    cv2.imshow("test",test)
    # img[:,:,0] =
    kernelSharpen = np.array([[-1, -1, -1, -1, -1],
                                 [-1, 2, 2, 2, -1],
                                 [-1, 2, 8, 2, -1],
                                 [-1, 2, 2, 2, -1],
                                 [-1, -1, -1, -1, -1]]) / 8.0

    # kernelSharpen = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    # img = cv2.filter2D(img,-1,kernelSharpen)
    # cv2.imshow("sharpen",img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # img = test
    # img = cv2.equalizeHist(img)

    # c2 = cv2.getTrackbarPos("c2", track)
    c3 = cv2.getTrackbarPos("c3", track)
    c4 = cv2.getTrackbarPos("c4", track)

    img = cv2.bilateralFilter(img, 10, c3, c4)  # Blur image, remove noise but keep edges

    c1 = cv2.getTrackbarPos("c1",track)
    # ret, img = cv2.threshold(img, c1, 255, cv2.THRESH_BINARY_INV)
    ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY)
    # th, img = cv2.threshold(img, c1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # ret, img = cv2.threshold(img, c1, 255, cv2.THRESH_TOZERO_INV)

    # pixels = cv2.getTrackbarPos("convert",track)
    kernel = np.ones((5, 5), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    # img = cv2.equalizeHist(img)

    img = autoCanny(img)
    # img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

    # img = cv2.bilateralFilter(img, 10, c3, c4)  # Blur image, remove noise but keep edges

    # lines = cv2.HoughLinesP(img,1,np.pi/180,100)
    # img = cv2.medianBlur(img,1)
    # img = cv2.Laplacian(img, cv2.CV_64F)
    # img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    # img = cv2.Sobel(img,10,c2,c3)
    # c3 = cv2.getTrackbarPos("c3", track)
    #
    # img = cv2.bilateralFilter(img, c1, c2, c3)  # Blur image, remove noise but keep edges

    # img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    # cv2.imshow("test",cv2.cvtColor(image,cv2.COLOR_BGR2GRAY))


    # ZNAJDYWANIE KOSCI
    dices = findSquares(img)
    # dices = None
    # img = findCircles(img)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if (dices is not None):
        for d in dices:
            # print(d)
            # cv2.drawContours(circle, [d], -1, (0, 0, 255), 3)
            cv2.drawContours(img, [d], -1, (0, 0, 255), 3)

    # if lines is not None:
    #     for x1,y1,x2,y2 in lines[0]:
    #         cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
    cv2.imshow(track,img)


def playCamera(camera):
    cap = cv2.VideoCapture(camera)
    while (True):
        check,klatka = cap.read()
        if check == True:

            # findDice(klatka)
            testowanie(klatka)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

def playImages():
    image = cv2.imread("./images/20.jpg")
    # cv2.imshow("obraz",image)
    # findDice(image)
    while True:
        testowanie(image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    playImages()
    # playCamera(0)