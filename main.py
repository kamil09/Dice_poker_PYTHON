from pip._vendor.distlib.compat import raw_input

from colors import bcolors
from dice_img_lib.dice_find import find_dices
from dice_lib import dice, ai

def run():
    print(bcolors.BOLD+"Let's play a game :)"+bcolors.ENDC)
    i=0
    c_points = 0
    p_points = 0
    while raw_input()!="exit" :
        i+=1
        print("STARTED GAME NUMBER:  "+str(i))
        c_points, p_points = playSimpleGame(c_points, p_points)
        print("COMPUTER: "+str(c_points)+" YOU: "+str(p_points))

def playSimpleGame(c_points, p_points):
    #PLAYER ONE - USER, PLAYER2 - COMPUTER
    player1 = 0
    player2 = 0
    print("\n>>Starting round 1\n")
    player1, player2 = playOneRound(player1, player2)
    print("\n>>Starting round 2\n")
    player1, player2 = playOneRound(player1, player2)
    if(player1-player2==2):
        p_points+=1
        print(bcolors.OKGREEN+"YOU WON!!!\n"+bcolors.ENDC)
        return c_points, p_points
    if(player2-player1==2):
        c_points+=1
        print(bcolors.FAIL+"COMPUTER WON!!!\n"+bcolors.ENDC)
        return c_points, p_points
    print("\n>>Starting round 3\n")
    player1, player2 = playOneRound(player1, player2)
    if (player1>player2):
        p_points += 1
        print(bcolors.OKGREEN+"YOU WON!!!\n"+bcolors.ENDC)
        return c_points, p_points
    if (player2>player1):
        c_points += 1
        print(bcolors.FAIL+"COMPUTER WON!!!\n"+bcolors.ENDC)
        return c_points, p_points
    print(bcolors.OKBLUE+"NO-ONE WON!!!\n"+bcolors.ENDC)
    return c_points, p_points

def playOneRound(pl1, pl2):
    raw_input()
    computerDices = dice.rand(5)
    #yourDices = dice.rand(5)
    print("COMPUTER DICES:")
    dice.printDicesInLine(computerDices, bcolors.YELL_BAC)

    while 1==1:
        raw_input(bcolors.OKBLUE+"Throw dices and press enter"+bcolors.ENDC)
        num, yourDices = find_dices()
        if(num == 5): break
        print("found "+str(num)+" dices instead of 5, try again")

    print("YOUR DICES:")
    dice.printDicesInLine(yourDices, bcolors.PLAYER)

    computerDices, retC = ai.simpleRethrow(computerDices)
    print("Computer Rethrow values: ", end="")
    print(retC)
    print("RETHROW YOUR DICES")
    while 1==1:
        raw_input(bcolors.OKBLUE+"Take from table dices you do not want to rethrow"+bcolors.ENDC)
        num, yourDicesToRethrow = find_dices()
        if (num <= 5): break
        print("dices not found")
    print("You rethrow values: ", end="")
    print(yourDicesToRethrow)

    yourDices2 = []
    for x in yourDices:
        if (x not in yourDicesToRethrow): yourDices2.append(x)
        for i, y in enumerate(yourDicesToRethrow):
            if(y==x):
                yourDicesToRethrow[i]=0
                break
    yourDices=yourDices2

    while 1==1:
        raw_input(bcolors.OKBLUE+"Rethrow dices"+bcolors.ENDC)
        num2, newDices = find_dices()
        if (num == num2): break
        print("found "+str(num2)+" dices instead of "+ str(num)+" , try again")
    for x in newDices: yourDices.append(x)

    print("COMPUTER DICES:")
    dice.printDicesInLine(computerDices, bcolors.YELL_BAC)
    print("YOUR DICES:")
    dice.printDicesInLine(yourDices, bcolors.PLAYER)
    winner = dice.checkWinner(yourDices, computerDices)
    if(winner == 1):
        print("You won this round")
        return pl1+1,pl2
    if(winner == 2):
        print("Computer won this round")
        return pl1, pl2+1
    print("DRAW!")
    return pl1,pl2

if __name__ == '__main__':
    run()