#Return number of dices and list of it's values
#How many dices we must find, if 0 - any number
import cv2
from dice_img_lib import camera as cam
from collections import defaultdict

def listToString(diceList):
    newString = ""
    for d in diceList:
        newString += "_" + str(d)
    return newString

def stringToList(string):
   stringList = string.split("_",1)
   diceList = []
   for s in stringList:
       diceList.append(int(s))
   return diceList


def find_dices(camera):
    cap = cv2.VideoCapture(camera)
    cap.set(3, 640)
    cap.set(4, 480)
    map = defaultdict(lambda : 0)
    for i in range(10):
        check, klatka = cap.read()
        kostki, _ = cam.findAndDraw(klatka)
        kostki = sorted(kostki)
        newHash = listToString(kostki)
        map[newHash] += 1
    cap.release()
    string = max(map.iterkeys(), key=(lambda key: map[key]))
    print(string)
    return stringToList(string)