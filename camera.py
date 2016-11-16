import cv2
import numpy as np

def findCircles(image):
    circles = cv2.HoughCircles(image,cv2.HOUGH_GRADIENT,1,40,param1=50,param2=30,minRadius=0,maxRadius=0)
    image = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
    if circles is None:
        return image
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2) #Outter circle
        cv2.circle(image,(i[0],i[1]),2,(255,0,0),3) #Center of a circle
    return image

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
    grey = cv2.bilateralFilter(grey, 1, 20, 20)  # Blur image, remove noise but keep edges
    edges = cv2.Canny(grey, 10, 200)
    image2, conturs, hierarchy = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # conturs = sorted(conturs,key = cv2.contourArea,reverse = True)[:20]
    diceContours = []
    for c in conturs:
        perimeter = cv2.arcLength(c, True)
        aprox = 0.02
        approximation = cv2.approxPolyDP(c, aprox * perimeter, True)
        if len(approximation) == 4:
            diceContours.append(approximation)

    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    # circle = findCircles(edges)
    for d in diceContours:
        # print(d)
        # cv2.drawContours(circle, [d], -1, (0, 0, 255), 3)
        cv2.drawContours(edges, [d], -1, (0, 0, 255), 3)
    # cv2.imshow("Circles",circle)
    cv2.imshow("edges",edges)


def playCamera(camera):
    cap = cv2.VideoCapture(camera)
    while (True):
        check,klatka = cap.read()
        if check == True:
            findDice(klatka)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # image = cv2.imread("dice.jpg")
    # cv2.imshow("obraz",image)
    # findDice(image)
    # cv2.waitKey(0)
    playCamera(0)