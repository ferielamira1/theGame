
from Player import Player
from Deck import Deck
import numpy as np
if __name__ == '__main__':


    deck = Deck()
    deck.shuffle()

    #define number of players
    while True:
        try:
            numberPlayers = int(input("Enter a number of players between 1-5: \n"))
            if not (numberPlayers in range(0,6)):
                print("The number of players must lay between 1-5")
                continue
            else:
                break
        except ValueError:
            print("This is not a number. Please enter a valid number")



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




    for player in players:
        mustPlay = True
        stillPlaying=True
        numberLayedCards=0




        while(gameOver == False
              and(stillPlaying == True
              or mustPlay == True)):



            print("The next player is {} \n".format(player.name))





            #check if hand contains a card that is smaller than downwards  or bigger than  upwards

            while(True):

                if (not (numberLayedCards < 2 and len(deck.cards) > 0) or (
                        numberLayedCards < 1 and len(deck.cards) == 0)):
                    mustPlay = False


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

                try:
                    player.showHand()
                    card = int(input("The stacked cards are currently in this state: \n Going UPWARDS: \n "
                              "1) \u2191 {} \n 2) \u2191 {} \n "
                              "Going DOWNWARDS: \n"
                              "3) \u2193 {} \n 4) \u2193 {} \n".format(deck.upwardPile[0],deck.upwardPile[1],deck.downwardPile[0],deck.downwardPile[1])
                              + "Enter the card to play: \n"))

                    if not (card in player.getHand()):
                        print("The card is  not in your hand.Please enter a valid card \n")
                        break

                except ValueError:
                    print("This is not a number. Please enter a valid number")


                result =  player.play(deck,card)
                numberLayedCards+=1


                if (player.emptyHand()==True):
                    gameOver == True
                    print("CONGRATULATIONS {}, YOU WON THE GAME!".format(player.name))
                    break

                if numberPlayers == 1 :
                    drawnCard = player.drawCard(deck)
                    print("You've drawn the card {} \n".format(drawnCard))


                elif numberLayedCards>=2 :
                    while True:
                        try:

                            stillPlaying = bool(int(input("Would you like to lay another card ? \n 1) no \n 2) yes \n")) - 1)
                            if stillPlaying == False and deck.isDeckEmpty() == False:
                                for _ in range(numberLayedCards+1):
                                    drawnCard = player.drawCard(deck)
                                    print("You've drawn the card {}".format(drawnCard))

                            break

                        except ValueError:
                            print("This is not a number. Please enter a valid number")


    totalCards = 0
    for player in players:
        totalCards += len(player.hand)


    if totalCards + len(deck.cards) <=10:

        print("CONGRATULATIONS,YOU HAVE AN EXCELLENT SCORE!")
    else:
        print("YOU DIED")









