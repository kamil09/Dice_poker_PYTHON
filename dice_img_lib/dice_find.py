#Return number of dices and list of it's values
#How many dices we must find, if 0 - any number

camera = 0

import cv2
from dice_img_lib import camera as cam
from collections import defaultdict

def listToString(diceList):
    newString = ""
    for d in diceList:
        newString += str(d) + "_"
    return newString

def stringToList(string):
    stringList = string.split("_")
    diceList = []
    stringList.remove("")
    print(stringList)
    for s in stringList:
        diceList.append(int(s))
    return diceList


def find_dices():
    cap = cv2.VideoCapture(camera)
    cap.set(3, 640)
    cap.set(4, 480)
    map = defaultdict(lambda : 0)
    for i in range(20):
        check, klatka = cap.read()
        kostki, _ = cam.findAndDraw(klatka)
        if(len(kostki) == 0): continue
        kostki = sorted(kostki)
        newHash = listToString(kostki)
        map[newHash] += 1
    cap.release()
    if(len(map) == 0 ): return 0,[]
    v = list(map.values())
    k = list(map.keys())
    string =  k[v.index(max(v))]
    print(string)
    dices = stringToList(string)
    return len(dices), dices