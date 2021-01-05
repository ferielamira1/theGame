import random

class Deck(object):
    def __init__(self):
        self.upwardPile=[[],[]]
        self.downwardPile=[[],[]]
        self.cards= []
        self.build()


    def build(self):

        self.upwardPile=[[1],[1]]
        self.downwardPile=[[100],[100]]

        for value in range(2,100):
            self.cards.append(value)


    def show(self):
        for card in self.cards:
            print(card)

    def shuffle(self):
        for i in range(len(self.cards)-1,0,-1):
            r = random.randint(0,i)
            self.cards[i],self.cards[r]=self.cards[r],self.cards[i]

    def draw_card(self):
        return self.cards.pop()

    def is_deck_empty(self):
        return True if len(self.cards)==0 else False


