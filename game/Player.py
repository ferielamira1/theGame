import math

import numpy as np
class Player(object):
    def __init__(self,id):
        self.id = id
        self.num_played_cards = 0
        self.hand=[]
        self.give_hint=False
        self.payoffs=[]


    def draw_hand(self, deck, numberPlayers):
        if numberPlayers in range(3,6):
            for i in range(1,7):
                self.hand.append(deck.draw_card())


        if numberPlayers==2:
            for i in range(1,8):
                self.hand.append(deck.draw_card())

        if numberPlayers==1:
            for i in range(1,9):
                self.hand.append(deck.draw_card())
        return self

    def draw_card(self, deck):
        if not deck.is_deck_empty():
            card = deck.draw_card()
        return card

    def show_hand(self):
        print("Player {} has hand: ".format(self.name))
        for card in self.hand:
            print("{} ".format(card),end="")

        print("\n")

    def empty_hand(self):
        return True if len(self.hand)==0 else False


    def get_hand(self):
        return self.hand

    def can_play(self,deck):
        hand = []
        for card in self.hand:
            if card != -1:
                hand.append(card)
        hand = np.array(hand)
        if len(hand)!= 0:
            if (hand > deck.upwardPile[0][len(deck.upwardPile[0])-1]).any() or (hand > deck.upwardPile[1][len(deck.upwardPile[1])-1]).any() or (
                    hand == deck.upwardPile[0][len(deck.upwardPile[0])-1] - 10).any() or (hand == deck.upwardPile[1][len(deck.upwardPile[1])-1] - 10).any() or (
                    hand < deck.downwardPile[0][len(deck.downwardPile[0])-1]).any() or (hand < deck.downwardPile[1][len(deck.downwardPile[1])-1]).any() or (
                    hand == deck.downwardPile[0][len(deck.downwardPile[0])-1] + 10).any() or (
                    hand == deck.downwardPile[1][len(deck.downwardPile[1])-1] + 10).any():
                return True
            else:
                return False
        else:
            return False



