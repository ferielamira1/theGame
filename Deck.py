import random

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
        return True if len(self.cards)==0 else False




    def computeDistance(self,pCards):
        smallest = [100, 100,0,0]

        for index, pile in enumerate(self.upwardPile):

            for card in pCards:
                if card > pile :
                    current = card
                    if current < smallest[index] :
                        smallest[index] = current


        for index, pile in enumerate(self.downwardPile):
            for card in pCards:
                if card < pile :
                    current = card
                    if current > smallest[2+index] :
                        smallest[2+index] = current


        distances = [smallest[0] - self.upwardPile[0],
                     smallest[1] - self.upwardPile[1],
                     self.downwardPile[0] - smallest[2],
                     self.downwardPile[1] - smallest[3]]

        indexCard  = distances.index(min(distances))
        if indexCard < 2:
            return smallest[indexCard],self.upwardPile[indexCard]

        else:
            return smallest[indexCard], self.upwardPile[indexCard-2 ]














class Card(object):
    def __init__(self):
        self.number = 0
        self.dis








