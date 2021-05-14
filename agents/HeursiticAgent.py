import numpy as np



class HeuristicAgent(object):

    ''' A random agent. Random agents is for running toy examples on the card games
    '''
    def __init__(self):
        self.action_num = 400



    def computeDistance(self, pCards, deck):
        smallest = [100, 100, 0, 0]

        for index, pile in enumerate(deck.upwardPile):

            for card in pCards:
                if card != -1 and (card > pile[len(pile)-1] or card == pile[len(pile)-1]-10):
                    current = card
                    if current < smallest[index] :
                        smallest[index] = current

        for index, pile in enumerate(deck.downwardPile):
            for card in pCards:
                if card != -1 and (card < pile[len(pile)-1] or card == pile[len(pile)-1]+10):
                    current = card
                    if current > smallest[2 + index]:
                        smallest[2 + index] = current

        distances = [smallest[0] - deck.upwardPile[0][len(deck.upwardPile[0])-1] if smallest[0]!=100 else np.inf,
                     smallest[1] - deck.upwardPile[1][len(deck.upwardPile[1])-1] if smallest[1]!=100 else np.inf,
                     deck.downwardPile[0][len(deck.downwardPile[0])-1] - smallest[2] if smallest[2]!=0 else np.inf,
                     deck.downwardPile[1][len(deck.downwardPile[1])-1] - smallest[3] if smallest[3]!=0 else np.inf]

        indexCard = distances.index(min(distances))
        return smallest[indexCard], indexCard


    def step(self,obs,legal_actions):
        ''' Predict the action given the curent state in gerenerating training data.
        Args:
            state (dict): An dictionary that represents the current state
        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
        '''

        deck = obs["deck"]

        hand = obs["player"].hand
        if 0 in legal_actions:
            return 0
        else:

            card, pile_n= self.computeDistance(hand,deck)

            action = (pile_n*100)+card
            return action

    def eval_step(self, obs,legal_actions):
        ''' Predict the action given the current state for evaluation.
            Since the random agents are not trained. This function is equivalent to step function
        Args:
            state (dict): An dictionary that represents the current state
        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
            probs (list): The list of action probabilities
        '''
        probs = [0 for _ in range(self.action_num)]
        for i in legal_actions:
            probs[i] = 1/len(legal_actions)
        return self.step(obs,legal_actions), probs
