from pip._vendor.distlib.compat import raw_input
import dice
from colors import bcolors
import ai

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
    yourDices = dice.rand(5)
    print("COMPUTER DICES:")
    dice.printDicesInLine(computerDices, bcolors.YELL_BAC)
    print("YOUR DICES:")
    dice.printDicesInLine(yourDices, bcolors.BLUE_BAC)
    print("RETHROW YOUR DICES")
    raw_input()
    computerDices, retC = ai.simpleRethrow(computerDices)
    yourDices, retY = ai.simpleRethrow(yourDices)
    print("Computer Rethrow values: ",end="")
    print(retC)
    print("You rethrow values: ",end="")
    print(retY)
    print("COMPUTER DICES:")
    dice.printDicesInLine(computerDices, bcolors.YELL_BAC)
    print("YOUR DICES:")
    dice.printDicesInLine(yourDices, bcolors.BLUE_BAC)
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