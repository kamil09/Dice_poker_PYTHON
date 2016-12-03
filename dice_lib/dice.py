import random
from colors import bcolors


def rand(number):
    dices = []
    for i in range(number):
        dices.append(random.randint(1,6))
    return dices

def checkPoker(diceList):
    if(len(set(diceList))==1): return True, diceList[0]
    return False, 0

def checkKareta(diceList):
    return checkCountHelper(diceList, 4)

def checkStrit(diceList):
    if(len(set(diceList))==5 and (max(diceList)-min(diceList)==4)):
        if(1 in diceList): return True, 1
        else: return True, 2
    return False, 0

def checkThree(diceList):
    return checkCountHelper(diceList, 3)

def check2pair(diceList):
    res, val = check1pair(diceList)
    if(res==False): return False, val
    res, val2 = check1pair(deleteFromList(diceList,val))
    if (res == True): return True, max([val2,val])*10 + min([val2,val])
    return False, 0

def checkFull(diceList):
    res, val = checkThree(diceList)
    if(res==False): return False, val
    res, val2 = check1pair( deleteFromList(diceList,val) )
    if(res==True): return True, val*10+val2
    return False, 0

def check1pair(diceList):
    return checkCountHelper(diceList, 2)

def checkNothing(diceList):
    return True, max(diceList)

def checkWinner(diceList1, diceList2):
    for fi, func in enumerate(__pokerFunctions__):
        res1, val1 = func(diceList1)
        res2, val2 = func(diceList2)
        if(res1==False and res2==False): continue
        if(res1==True and res2==False): return 1
        if(res2==False and res2==True): return 2
        #The same figures
        if(val1>val2): return 1
        if(val2>val1): return 2
        #The same figures and values
        diceList1 = __deleteFigures__[fi](diceList1,val1)
        diceList2 = __deleteFigures__[fi](diceList2,val2)
    return 0 #Remis

def checkCountHelper(diceList, num):
    sum = [0, 0, 0, 0, 0, 0, 0]
    for i in diceList: sum[i] += 1
    for i, k in enumerate(sum):
        if (k == num): return True, i
    return False, 0

def deleteFromList(diceList, num):
    newDiceList = []
    for i in diceList:
        if (i != num): newDiceList.append(i)
    return newDiceList

def simpleFDel(diceList, num):
    if(num<=6): return deleteFromList(diceList, num)
    else: return deleteFromList(deleteFromList(diceList, (num-(num%10))/10) , (num%10) )

def returnEmptyArray(diceList, num):
    return []

__pokerFunctions__  = [checkPoker, checkKareta, checkFull, checkStrit, checkThree, check2pair, check1pair, checkNothing]
__deleteFigures__   = [returnEmptyArray, simpleFDel, returnEmptyArray, returnEmptyArray, simpleFDel, simpleFDel, simpleFDel, simpleFDel ]

diceShow = [
    ["|     |","|x    |","|x    |", "|x   x|","|x   x|","|x   x|"],
    ["|  x  |","|     |","|  x  |", "|     |","|  x  |","|x   x|"],
    ["|     |","|    x|","|    x|", "|x   x|","|x   x|","|x   x|"]
]

def printDicesInLine(dicesList, colorStr=""):
    for i in range(3):
        print(bcolors.BOLD+colorStr+"\t\t",end="")
        for k in dicesList:
            print(diceShow[i][k-1]+"  ", end="")
        print(""+bcolors.ENDC)
