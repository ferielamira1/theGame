import math

class Player(object):
    def __init__(self,name):
        self.name = name
        self.hand=[]




    def action(self,deck,pCards, choices):

        for index,c in enumerate(choices):
            if c == 1:
                choice=index

        # we can set choice randomly
        print("CHOICE {}".format(choice))
        if (choice == 0 or  choice == 1) :

            smallest = math.inf

            # play card on upDeck1
            for card in pCards:
                if card > deck.upwardPile[choice]:
                    current = card
                    if current < smallest:
                        smallest = current

            if (smallest == math.inf):
                print("Could not play card")
                return False

            else :
                deck.upwardPile[choice] = smallest
                self.hand.remove(smallest)
                if not deck.isDeckEmpty():
                    self.drawCard(deck)
                print("Successfully played card")
                return True

        if choice == 2 or choice == 3:
            smallest = 0

            for card in pCards:
                if card < deck.downwardPile[choice-2]:
                    current = card

                    if current > smallest:
                        smallest= current

            if (smallest == 0):
                print("Could not play card")
                return False
            else :
                deck.downwardPile[choice-2] = smallest

                self.hand.remove(smallest)
                if not deck.isDeckEmpty():

                    self.drawCard(deck)

                print("Successfully played card")

                return True




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
        if not deck.isDeckEmpty():
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

    #returns True if player was able to play
    #returns false otherwise


    def play(self,deck,pCards):
            smallest = [math.inf, math.inf, 0, 0]

            for index, pile in enumerate(deck.upwardPile):
                for card in pCards:
                    if card > pile:
                        current = card
                        if current < smallest[index]:
                            smallest[index] = current



            for index, pile in enumerate(deck.downwardPile):
                for card in pCards:
                    if card < pile:
                        current = card

                        if current > smallest[2 + index]:
                            smallest[2 + index] = current

            if (smallest == [math.inf, math.inf, 0, 0]):
                return False

            else:
                for i,s in enumerate(smallest):
                    if s == 0:
                        smallest[i] = math.inf
                distances = [smallest[0] - deck.upwardPile[0],
                             smallest[1] - deck.upwardPile[1],
                             abs(deck.downwardPile[0] - smallest[2]),
                             abs(deck.downwardPile[1] - smallest[3])]

                indexCard = distances.index(min(distances))

                if indexCard < 2:

                    deck.upwardPile[indexCard] = smallest[indexCard]

                    self.hand.remove(smallest[indexCard])

                else:
                    deck.downwardPile[indexCard -2] = smallest[indexCard]

                    self.hand.remove(smallest[indexCard])
                return True


    def getHand(self):
        return self.hand

