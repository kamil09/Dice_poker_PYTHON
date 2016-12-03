from dice_lib import dice


#Return newList, listOfRethrowDices
def simpleRethrow(myDices):
    for fi, func in enumerate(dice.__pokerFunctions__):
        res, val = func(myDices)
        if(res == True):
            toRethrow = dice.__deleteFigures__[fi](myDices, val)
            if(len(toRethrow)==0): return myDices, []
            returnDices = dice.rand(len(toRethrow))
            for x in myDices:
                if(x not in toRethrow): returnDices.append(x)
            return returnDices, toRethrow
    return "NOT POSSIBLE TO RETURN THIS"



