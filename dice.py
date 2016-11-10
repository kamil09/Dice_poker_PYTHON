import random

def rand(number):
    dices = []
    for i in range(number):
        dices.append(random.randint(1,6))
    return dices

def checkPoker(diceList):
    if(len(diceList)!=5): return False, -1
    if(len(set(diceList))==1): return True, diceList[0]
    return False, 0

def checkKareta(diceList):
    return checkCountHelper(diceList, 4)

def checkStrit(diceList):
    if(len(diceList)!=5): return False, -1
    if(len(set(diceList))==5):
        if(1 in diceList): return True, 1
        else: return True, 2
    return False, 0

def checkThree(diceList):
    return checkCountHelper(diceList, 3)

def check2pair(diceList):
    if(len(diceList)!=5): return False, -1
    res, val = check1pair(diceList)
    if(res==False): return False, val
    newDiceList = []
    for i in diceList:
        if (i != val): newDiceList.append(i)
    res, val2 = check1pair(diceList)
    if (res == True): return True, max([val2,val])*10 + min([val2,val])
    return False, 0

def checkFull(diceList):
    res, val = checkThree(diceList)
    if(res==False): return False, val
    newDiceList = []
    for i in diceList:
        if(i!=val): newDiceList.append(i)
    res, val2 = check1pair(diceList)
    if(res==True): return True, val2*10+val
    return False, 0

def check1pair(diceList):
    return checkCountHelper(diceList, 2)

def checkNothing(diceList):
    if(len(diceList)!=5): return False, -1
    return True, max(diceList)

pokerFunctions = [checkPoker, checkKareta, checkFull, checkStrit, checkThree, check2pair, check1pair, checkNothing]

def checkCountHelper(diceList, num):
    if(len(diceList)!=5): return False, -1
    sum = [0, 0, 0, 0, 0, 0]
    for i, k in range(diceList): sum[i] += 1
    for i in sum:
        if (k == num): return True, i
    return False, 0
