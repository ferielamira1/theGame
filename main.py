
from Player import Player
from Deck import Deck
import numpy as np
import sys
if __name__ == '__main__':

    if len(sys.argv) <2 :
        raise ValueError("You need to set the number of players.")
    else:
        if ( (not str.isdigit(sys.argv[1])) or (not (int(sys.argv[1])in range(-1,6)))):
            raise ValueError("You need to set the number of players between 1-5")

        deck = Deck()
        deck.shuffle()

        numberPlayers = int(sys.argv[1])  #int(input("Enter a number of players between 1-5: \n"))


        players = []

        for i in range(1,numberPlayers+1):
            name = input("Enter player {}'s name: \n".format(i))
            p = Player(name)
            p.drawHand(deck, numberPlayers)
            p.showHand()
            players.append(p)


        gameOver = False

        print("*****************************************************")
        print("******************THE GAME STARTED*******************")
        print("*****************************************************")
        while(gameOver==False):
            for player in players:
                mustPlay = True
                stillPlaying=True
                numberLayedCards=0

                while(gameOver == False
                      and(stillPlaying == True
                      or mustPlay == True)):



                    print("The next player is {} \n".format(player.name))


                    #check if hand contains a card that is smaller than downwards  or bigger than  upwards

                    if (not (numberLayedCards < 2 and len(deck.cards) > 0) or (
                            numberLayedCards < 1 and len(deck.cards) == 0)):
                        mustPlay = False
                        print("Player can stop")


                    if (mustPlay and (all( (card > deck.downwardPile[0]for card in player.hand))
                                      and all(card > deck.downwardPile[1] for card in player.hand)
                                      and all(card < deck.upwardPile[0] for card in player.hand)
                                      and all(card < deck.upwardPile[1] for card in player.hand)
                                      and all(card != deck.downwardPile[0] +10 for card in player.hand)
                                      and all(card != deck.downwardPile[1] +10 for card in player.hand)
                                      and all(card != deck.upwardPile[0] -10 for card in player.hand)
                                      and all(card != deck.upwardPile[1] -10 for card in player.hand))):
                        gameOver = True
                        break


                    player.showHand()

                    print("The stacked cards are currently in this state: \n Going UPWARDS: \n "
                        "1) \u2191 {} \n 2) \u2191 {} \n "
                        "Going DOWNWARDS: \n"
                        "3) \u2193 {} \n 4) \u2193 {} \n".format(deck.upwardPile[0],deck.upwardPile[1],deck.downwardPile[0],deck.downwardPile[1]))

                    card = deck.computeDistance(player.hand)

                    result = player.play(deck,player.hand)

                    if result:
                        numberLayedCards += 1

                    if not result:
                        stillPlaying = False
                        if (numberLayedCards<2 and deck.isDeckEmpty()==False) or (numberLayedCards<1 and deck.isDeckEmpty()==True):
                            gameOver = True
                            break



                    if numberPlayers == 1:
                        drawnCard = player.drawCard(deck)
                        print("You've drawn the card {} \n".format(drawnCard))


                    elif numberLayedCards>2 :
                        if stillPlaying==False:
                            for _ in range(numberLayedCards):
                                if not deck.isDeckEmpty():
                                    drawnCard = player.drawCard(deck)
                                    print("You've drawn the card {}".format(drawnCard))




        totalCards = 0
        for player in players:
            totalCards += len(player.hand)
        if totalCards + len(deck.cards) <=10:

            print("CONGRATULATIONS,YOU HAVE AN EXCELLENT SCORE!")
        else:
            print("YOU DIED WITH SCORE: {}".format(totalCards + len(deck.cards)))









