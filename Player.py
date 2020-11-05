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
            print("{} ".format(card),end="")

        print("\n")

    def emptyHand(self):
        return True if len(self.hand)==0 else False

    def play(self,deck,card):


        #on which pile ?
        while(True):

            try:
                pileNumber = int(input("On which pile of cards would you like to play?  \n"))

                if(pileNumber == 1 or pileNumber ==2):
                    #UPWARDS
                    if(card > deck.upwardPile[pileNumber-1] or (card == deck.upwardPile[pileNumber-1] - 10 )):
                        deck.upwardPile[pileNumber-1]=card
                        self.hand.remove(card)
                        break
                    else:
                        print("The handed card is smaller than the top of the stack")

                if(pileNumber == 3 or pileNumber ==4):
                    # DOWNWARDS
                    if (card < deck.downwardPile[pileNumber-3] or (card == deck.upwardPile[pileNumber-3] + 10 )):

                        deck.downwardPile[pileNumber-3] = card
                        self.hand.remove(card)
                        break
                    else:
                        print("The handed card is bigger than the top of the stack")

                else:
                    print("The number must lay between 1-4. Please enter a valid number ")
            except ValueError:
                print("This is not a number. Please enter a valid number")


    def getHand(self):
        return self.hand

