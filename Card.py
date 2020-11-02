import random

#class Card(object):
#    def __init__(self,val):
#        self.value = val


#    def show(self):
#        print("{}".format(self.value))


class Deck(object):
    def __init__(self):
        self.upwardPile=[]
        self.downwardPile=[]
        self.cards= []
        self.build()

    def build(self):

        self.upwardPile=[1,1]
        self.downwardPile=[100,100]

        for value in range(2,100):
            self.cards.append(value)

    def show(self):
        for card in self.cards:
            print(card)

    def shuffle(self):
        for i in range(len(self.cards)-1,0,-1):
            r = random.randint(0,i)
            self.cards[i],self.cards[r]=self.cards[r],self.cards[i]

    def drawCard(self):

        return self.cards.pop()

    def isDeckEmpty(self):
        return True if len(self.cards)!=0 else False




class Player(object):
    def __init__(self,name):
        self.name = name
        self.hand=[]

    def drawHand(self,deck,numberPlayers):
        if numberPlayers in range(3,6):
            for i in range(1,7):
                self.hand.append(deck.drawCard())

        if (numberPlayers==2):
            for i in range(1,8):
                self.hand.append(deck.drawCard())

        if (numberPlayers==1):
            for i in range(1,9):
                self.hand.append(deck.drawCard())
        return self

    def drawCard(self,deck):
        card = deck.drawCard()
        self.hand.append(card)
        return card

    def showHand(self):
        print("Player {} has hand: ".format(self.name))
        for card in self.hand:
            print(card)

    def emptyHand(self):
        return True if len(self.hand)==0 else False

    def play(self,deck,card):

        #on which pile ?
        pileNumber = int(input("On which pile of cards would you like to play?  \n  "
                      "Going UPWARDS: \n "
                      "1) {} \n 2) {} \n "
                      "Going DOWNWARDS: \n"
                      "3) {} \n 4) {} \n".format(deck.upwardPile[0],deck.upwardPile[1],deck.downwardPile[0],deck.downwardPile[1])))

        if(pileNumber == (1 or 2)):
            #UPWARDS
            if(card > deck.upwardPile[pileNumber-1] or (card == deck.upwardPile[pileNumber-1] - 10 )):

                deck.upwardPile[pileNumber-1]=card
                self.hand.remove(card)
                if deck.isDeckEmpty() == False:
                    self.drawCard(deck)


            else:
                return ValueError("The handed card is smaller than the top of the stack")
        else:
            # DOWNWARDS
            if (card < deck.downwardPile[pileNumber-3] or (card == deck.upwardPile[pileNumber-1] + 10 )):

                deck.downwardPile[pileNumber-3] = card
                self.hand.remove(card)
                if deck.isDeckEmpty()==False :
                    self.drawCard(deck)
            else:
                return ValueError("The handed card is bigger than the top of the stack")




    def getHand(self):
        return self.hand





if __name__ == '__main__':

    #four cards placed in the center
    up1,up2,down1,down2=1,1,100,100

    #shuffle deck
    deck = Deck()
    deck.shuffle()

    #define number of players
    numberPlayers = int(input("Enter a number of players between 1-5: \n"))
    if numberPlayers not in range(1,6):
        raise ValueError("The number of players must lay between 1-5")

    players = []

    for i in range(1,numberPlayers+1):
        name = input("Enter player {}'s name: \n".format(i))
        p = Player(name)
        p.drawHand(deck,numberPlayers)
        p.showHand()
        players.append(p)


    gameOver = False
    for player in players:

        stillPlaying=False
        numberLayedCards=0


        while(gameOver == False
              and(stillPlaying == True and numberLayedCards< len(p.hand))
              or (numberLayedCards<2 and len(deck.cards)>0)
              or (numberLayedCards < 1 and len(deck.cards)==0)):
            card = int(input("The stacked cards are currently in this state: \n Going UPWARDS: \n "
                      "1) {} \n 2) {} \n "
                      "Going DOWNWARDS: \n"
                      "3) {} \n 4) {} \n".format(deck.upwardPile[0],deck.upwardPile[1],deck.downwardPile[0],deck.downwardPile[1])
                      + "Enter the card to play: \n"))


            if not(card in player.getHand()):
                raise ValueError("The card is  not in your hand \n")
            else:
                player.play(deck,card)
                numberLayedCards+=1
                # what happens in case the player cant  place ANY card on any of the piles ?

            if (player.emptyHand()==True):
                gameOver == True
                print("CONGRATULATIONS {}, YOU WON THE GAME!".format(player.name))
                break


            if int(input("Would you like to lay another card ? \n 1) yes \n 2) no"))==2:
                    stillPlaying=False


















