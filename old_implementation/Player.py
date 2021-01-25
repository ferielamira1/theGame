import math

import numpy as np
class Player(object):
    def __init__(self,name):
        self.name = name
        self.hand=[]
    #
    # def action(self, deck, move):
    #     """
    #     :param deck: Class, containing the piles and remainig cards in the deck
    #     :param move: Integer representing the chosen move
    #                 move in 0-3]: play card 0 on deck
    #     :return: True if game is over, else False
    #     """
    #
    #     if move == 32:
    #         return False
    #
    #     card_index = int(move / 4)
    #     pile = move % 4
    #
    #     card = self.hand[card_index]
    #
    #     if pile == 0 or pile == 1:
    #         if ((card > deck.upwardPile[pile][len(deck.upwardPile[pile])-1]) or (card == deck.upwardPile[pile][len(deck.upwardPile[pile])-1] - 10)) and card != -1:
    #             old_pile = deck.upwardPile[pile][len(deck.upwardPile[pile])-1]
    #             deck.upwardPile[pile].append(card)
    #
    #
    #             if deck.is_deck_empty():
    #                 self.hand[card_index] = -1
    #             else:
    #                 self.hand[card_index] = self.draw_card(deck)
    #             print("Successfully played card {}".format(card))
    #
    #             return True
    #
    #         else:
    #             print("Could not play card")
    #             return False
    #
    #     if pile == 2 or pile == 3:
    #         if ((card < deck.downwardPile[pile - 2][len(deck.downwardPile[pile-2])-1]) or (card == deck.downwardPile[pile - 2][len(deck.downwardPile[pile-2])-1] + 10)) and card != -1:
    #
    #             old_pile = deck.downwardPile[pile - 2][len(deck.downwardPile[pile-2])-1]
    #             deck.downwardPile[pile - 2].append(card)
    #             if deck.is_deck_empty():
    #                 self.hand[card_index] = -1
    #             else:
    #                 self.hand[card_index] = self.draw_card(deck)
    #
    #             print("Successfully played card {}".format(card))
    #
    #             return True
    #
    #         else:
    #             print("Could not play card")
    #             return False

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


