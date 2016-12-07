from dice_img_lib import camera
import numpy as np
import cv2

def checkImages():
    coverageMatrix = []
    allCorrect = 0.0
    allWrong = 0.0
    allMissed = 0.0
    srednia = 0.0
    for i in range(65):
        fileName = "images/"+str(i+1)
        image = cv2.imread(fileName+".jpg")
        if (image is None): continue

        kostki,middlePoints = camera.findAndDraw(image)
        print(kostki)
        test = cv2.imread(fileName+"test.png")
        correct,wrong,missed = checkRectangle(test,middlePoints)

        krotka = [correct,wrong,missed]

        coverageMatrix.append(krotka)

        allCorrect += correct
        allWrong += wrong
        allMissed += missed
        srednia += (correct-wrong)/(correct+missed)
        #print(str(b)+". &"+str(correct)+"&"+str(wrong)+"&"+str(missed)+"\\\\")
        #while True:
         #   if cv2.waitKey(1) & 0xFF == ord('q'): break
    #print(str(b) + ". &" + str(allCorrect) + "&" + str(allWrong) + "&" + str(allMissed) + "\\\\")
    result = srednia/len(coverageMatrix)
    print(result)
    cv2.destroyAllWindows()
    return result

def checkRectangle(image,points):
    middlePoints = points
    dices = camera.findSquares(cv2.cvtColor(image,cv2.COLOR_BGR2GRAY))
    correct = 0
    wrong = 0
    middleDices = []
    for d in dices:
        rect = camera.getRect(d)
        middle = camera.getMiddlePoint(rect)
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

    #image = cv2.resize(image, None, fx=800 / image.shape[1], fy=600 / image.shape[0], interpolation=cv2.INTER_CUBIC)
    #cv2.imshow("TEST",image)
    return correct,wrong,missed