from pip._vendor.distlib.compat import raw_input
import dice
import ai

def run():
    print("Let's play a game :)")
    i=0
    while raw_input()!="exit" :
        i+=1
        print("STARTED GAME NUMBER:  "+str(i))
        playSimpleGame()
    print("END! PS. I am no-one")

def playSimpleGame():
    #PLAYER ONE - USER, PLAYER2 - COMPUTER
    player1 = 0
    player2 = 0
    print("\n>>Starting round 1\n")
    player1, player2 = playOneRound(player1, player2)
    print("\n>>Starting round 2\n")
    player1, player2 = playOneRound(player1, player2)
    if(player1-player2==2):
        print("YOU WON!!!\n")
        return
    if(player2-player1==2):
        print("COMPUTER WON!!!\n")
        return
    print("\n>>Starting round 3\n")
    player1, player2 = playOneRound(player1, player2)
    if (player1>player2):
        print("YOU WON!!!\n")
        return
    if (player2>player1):
        print("COMPUTER WON!!!\n")
        return
    print("NO-ONE WON!!!\n")

def playOneRound(pl1, pl2):
    raw_input()
    computerDices = dice.rand(5)
    yourDices = dice.rand(5)
    print("COMPUTER DICES:")
    dice.printDicesInLine(computerDices)
    print("YOUR DICES:")
    dice.printDicesInLine(yourDices)
    print("RETHROW YOUR DICES")
    raw_input()
    computerDices, retC = ai.simpleRethrow(computerDices)
    yourDices, retY = ai.simpleRethrow(yourDices)
    print("Computer Rethrow values: ",end="")
    print(retC)
    print("You rethrow values: ",end="")
    print(retY)
    print("COMPUTER DICES:")
    dice.printDicesInLine(computerDices)
    print("YOUR DICES:")
    dice.printDicesInLine(yourDices)
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