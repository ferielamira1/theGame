
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






    gameOver = True

    print("*****************************************************")
    print("******************THE GAME STARTED*******************")
    print("*****************************************************")




    for player in players:

        stillPlaying=True
        numberLayedCards=0

        if any( (card < deck.downwardPile[0] or card < deck.downwardPile[1]  or
                  card > deck.upwardPile[0] or card > deck.upwardPile[1]) for card in player.hand ):




            while(gameOver == False
                  and(stillPlaying == True)
                  or (numberLayedCards<2 and len(deck.cards)>0)
                  or (numberLayedCards < 1 and len(deck.cards)==0)):

                print("The next player is {} \n".format(player.name))
                player.showHand()


                #check if hand contains a card that is smaller than downwards  or bigger than  upwards

                while(True):
                    try:
                        card = int(input("The stacked cards are currently in this state: \n Going UPWARDS: \n "
                                  "1) \u2191 {} \n 2) \u2191 {} \n "
                                  "Going DOWNWARDS: \n"
                                  "3) \u2193 {} \n 4) \u2193 {} \n".format(deck.upwardPile[0],deck.upwardPile[1],deck.downwardPile[0],deck.downwardPile[1])
                                  + "Enter the card to play: \n"))
                        if not (card in player.getHand()):
                            print("The card is  not in your hand.Please enter a valid card \n")
                        else:
                            break
                    except ValueError:
                        print("This is not a number. Please enter a valid number")



                result =  player.play(deck,card)
                numberLayedCards+=1
                # what happens in case the player cant  place ANY card on any of the piles ?

                if (player.emptyHand()==True):
                    gameOver == True
                    print("CONGRATULATIONS {}, YOU WON THE GAME!".format(player.name))
                    break

                if numberPlayers == 1 :
                    drawnCard = player.drawCard(deck)
                    print("You've drawn the card {}".format(drawnCard))

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
        else:
            print("You lost The Game.")
            break






