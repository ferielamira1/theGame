"""
Copyright (c) 2019 DATA Lab at Texas A&M University

Permission is hereby granteds, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

from rlcard.utils import *
from game.Player import Player
from game.Deck import Deck
import random



class Env(object):
    '''
    The base Env class. For all the environments in RLCard,
    we should base on this class and implement as many functions
    as we can.
    '''





    def __init__(self, config):
        ''' Initialize the environment
        Args:
            config (dict): A config dictionary. All the fields are
                optional. Currently, the dictionary includes:
                'seed' (int) - A environment local random seed.
                'env_num' (int) - If env_num>1, the environment wil be run
                  with multiple processes. Note the implementation is
                  in `vec_env.py`.
                'allow_step_back' (boolean) - True if allowing
                 step_back.
                'allow_raw_data' (boolean) - True if allow
                 raw obs in state['raw_obs'] and raw legal actions in
                 state['raw_legal_actions'].
                'single_agent_mode' (boolean) - True if single agent mode,
                 i.e., the other players are pretrained models.

                'current_player' (int) - If 'singe_agent_mode' is True,
                 'current_player' specifies the player that does not use
                  pretrained models.
                There can be some game specific configurations, e.g., the
                number of players in the game. These fields should start with
                'game_', e.g., 'game_player_num' which specify the number of
                players in the game. Since these configurations may be game-specific,
                The default settings should be put in the Env class. For example,
                the default game configurations for Blackjack should be in
                'rlcard/envs/blackjack.py'
                TODO: Support more game configurations in the future.
        '''
        # self.allow_step_back =  config['allow_step_back']
        # self.allow_raw_data = config['allow_raw_data']
        self.record_action = config['record_action']
        # self.single_agent_mode = config['single_agent_mode']
        self.current_player = None
        self.player_num = config['player_num']
        self.state_shape = config['state_shape']
        self.number_actions = config['number_actions']
        self.heuristic_communication = config['heuristic_communication']
        self.obs = {}
        self.agents: []
        if self.record_action:
            self.action_recorder = []
        self.strategy= config['strategy']
        self.hints=[]
        self.timestep = 0
        # Set random seed, default is None
        self._seed(config['seed'])
        self.players = []

    def step(self, action):
        ''' Step forward
        Args:
            action (int): The action taken by the current player

        Meaning of an action:
            0: pass, 		1:hint 1, 		2->99: play card x on upward deck 1
             		        101:hint 2,	    102->199:  upward deck 2
            		        201:hint 3,	    202-> 299: down1
            		        301:hint 4,	    302->399: down2
        Returns:
            (tuple): Tuple containing:
                (dict): The next observations
                (int): The ID of the next player
        '''

        self.timestep += 1
        # Record the action for human interface
        if self.record_action:
            self.action_recorder.append([self.get_player_id(), action])

        deck = self.obs["deck"]
        player = self.obs["player"]

        score = 0

        if action in [1,101,201,301]:
            if len(self.hints)>=2:
                self.hints=[]

            self.hints.append(int(action /100) )

            player.give_hint=False
            next_player = self.players[(player.id + 1) % len(self.players)]
            next_obs = {"player": next_player, "deck": deck, "others": np.delete(self.players, next_player.id)}
            self.obs = next_obs

            return self._extract_state(next_obs), next_player.id, score

        if action == 0:


            while player.num_played_cards!=0:
                if not deck.is_deck_empty():
                    for i in range(len(player.hand)):
                        if player.hand[i]== -1:
                            player.hand[i] = player.draw_card(deck)
                player.num_played_cards = player.num_played_cards - 1
            if self.strategy=="informative":

                player.give_hint=True

                return self._extract_state(self.obs), self.current_player.id, score

            else:

                next_player = self.players[(player.id + 1) % len(self.players)]


                next_obs = {"player": next_player, "deck": deck, "others": np.delete(self.players,next_player.id)}

                self.obs = next_obs

                return self._extract_state(next_obs), next_player.id, score


        card = int(action % 100)

        pile= int(action/100)

        if pile == 0 or pile == 1:
            if ((card > deck.upwardPile[pile][len(deck.upwardPile[pile]) - 1]) or (
                    card == deck.upwardPile[pile][len(deck.upwardPile[pile]) - 1] - 10)) and card != -1:

                if (card == deck.upwardPile[pile][len(deck.upwardPile[pile]) - 1] - 10):
                    score = 1
                else:
                    score = 1 / abs(card - deck.upwardPile[pile][len(deck.upwardPile[pile]) - 1])
                #score=1
                deck.upwardPile[pile].append(card)
                player.hand[player.hand.index(card)] = -1



        if pile == 2 or pile == 3:
            if ((card < deck.downwardPile[pile - 2][len(deck.downwardPile[pile - 2]) - 1]) or (
                    card == deck.downwardPile[pile - 2][len(deck.downwardPile[pile - 2]) - 1] + 10)) and card != -1:
                if card == deck.downwardPile[pile - 2][len(deck.downwardPile[pile - 2]) - 1] + 10:
                    score = 1
                else:
                    score = 1 / abs(card - deck.downwardPile[pile - 2][len(deck.downwardPile[pile - 2])- 1])
                #score=1
                deck.downwardPile[pile - 2].append(card)
                player.hand[player.hand.index(card)] = -1



        next_obs = {"player": player, "deck": deck, "others":[p for p in self.players if p != player] }

        player.num_played_cards += 1

        #print("PLAYER {} DID MOVE {}".format(player.id,action))
        self.obs = next_obs
        #print("DECK: \n   UP: {} \n   DOWN: {}\n".format(deck.upwardPile,deck.downwardPile))
        #print("CURRENT PLAYER {} \n   HAND :{}".format(player.id,player.hand))
        return self._extract_state(self.obs), self.current_player.id, score

    def set_agents(self, agents):
        '''
        Set the agents that will interact with the environment.
        This function must be called before `run`.
        Args:
            agents (list): List of Agent classes
        '''
        self.agents = agents



    def get_hints(self, coplayers):
        for p in coplayers:
            # if the player has a card that is -10 or has a card that is 1-2 under, send a hint
            deck = self.obs["deck"]

            upile1 = deck.upwardPile[0]
            upile2 = deck.upwardPile[1]
            dpile1 = deck.downwardPile[0]
            dpile2 =deck.downwardPile[0]
            hints=[]

            if any(abs(c - upile1[len(upile1) - 1]) == 1 or upile1[len(upile1) - 1] - c == 10  for c in p.hand):
                hints.append(0)

            if any(c == upile2[len(upile2) - 1] or upile2[len(upile2) - 1] - c == 10 for c in p.hand):
                hints.append(1)

            if any(c == dpile1[len(dpile1) - 1] or dpile1[len(dpile1) - 1] - c == -10 for c in p.hand):
                hints.append(2)

            if any(c == dpile2[len(dpile2) - 1] or dpile2[len(dpile2) - 1] - c == -10 for c in p.hand):
                hints.append(3)
        return hints

    def run(self, is_training=False):
        '''
        Run a complete game, either for evaluation or training RL agent.
        Args:
            is_training (boolean): True if for training purpose.
        Returns:
            (tuple) Tuple containing:
                (list): A list of trajectories generated from the environment.
                (list): A list payoffs. Each entry corresponds to one player.
        Note: The trajectories are 3-dimension list. The first dimension is for different players.
              The second dimension is for different transitions. The third dimension is for the contents of each
              transiton
        STATE:
            Upward pile 1	    0: dont play here          1:?         2-98: cards
            Upward pile 2	    100: don't play here       101:?       102-298:cards
            Downward pile 1 	200: don't play here       201:?       202-298:cards
            Downward pile 2	    300: don't play here       301:?       302-398:cards
            Player hand	        400:?                      401:?       402-498



            ACTION:
            0: pass, 		 1:  H1, 		  2->98:  play card x on upward deck 1
            100: ?, 		101: H2,	    102->198: downward deck 1
            200: ?,		    201: H3,	    202->298: up deck 2
            300: ?,		    301: H4,	    302->398: down deck


        '''

        trajectories = [[] for _ in range(self.player_num)]
        state, player_id = self._init_game()

        # Loop to play the game
        trajectories[player_id].append(state)
        score = 0
        while not self.is_over():

            # Agent plays


            if self.player_num>1 and self.strategy == 'h_informative' :

                    coplayers = np.delete(self.players,self.current_player.id)
                    self.hints= self.get_hints(coplayers)

                    for h in self.hints:
                        state[h][0]=1
            if self.player_num>1 and self.strategy == 'informative' :
                    if len(self.hints)>=1:
                        for h in self.hints[-2:]:
                            state[h][0]=1

            if not is_training:
                action, _ = self.agents[player_id].eval_step(state, self._get_legal_actions())
            else:
                action = self.agents[player_id].step(state, self._get_legal_actions())

            # Environment steps
            self.players[player_id].active=True
            next_state, next_player_id, payoff = self.step(action)
            if payoff>0:
                score += 1


            # Save action
            trajectories[player_id].append(action)
            self.agents[player_id].payoffs.append(payoff)

            # Set the state and player
            state = next_state
            player_id = next_player_id
            self.current_player= self.players[player_id]

            if not self.is_over():
                trajectories[player_id].append(state)



        # Add a final state to all the players
        for player_id in range(self.player_num):
            state = self.get_state(player_id)
            trajectories[player_id].append(state)

        # Payoffs
        payoffs = self.get_payoffs(score)

        # Reorganize the trajectories
        trajectories = reorganize(trajectories, payoffs)




        return trajectories, payoffs



    def is_over(self):
        ''' Check whether the curent game is over
        Returns:
            (boolean): True if current game is over
        '''

        player = self.obs["player"]
        deck = self.obs["deck"]
        if player.can_play(deck) or (player.num_played_cards>=2 and deck.is_deck_empty()==False) or (player.num_played_cards>=1 and deck.is_deck_empty()==True):
            return False
        else:

            #for p in self.players:
            #    print("PLAYER: {}, HAND: {}".format(p.id,p.hand))

            #print("**********GAME OVER***********")

            return True

    def get_player_id(self):
        ''' Get the current player id
        Returns:
            (int): The id of the current player
        '''
        return self.obs["player"].id

    def get_payoffs(self, score):
        '''Returns:
            (list): A list of payoffs for each player.

            Each payoff is between [1,-1]:
                if all cards were played then the payoffs are set to one,
                if more than 50% of the cards were played the payoffs are a positive value between ]0,1]
                otherwise, the payoffs will be a negative value between [-1,0[
        '''
        payoffs = np.array((1, self.player_num))

        '''
        if self.obs["deck"].is_deck_empty() and len(self.obs["player"].hand)==0:
            payoffs =  np.array([1.0 for i in range(self.player_num)])
        else:
            payoffs = np.array([score / 98 for i in range(self.player_num)])

        if len(self.obs["deck"].cards) > 49:

            payoffs = np.array([(score / 98)-1 for i in range(self.player_num)])
            
        '''

        num_handcards=0
        for p in self.players:
            num_handcards+=len(p.hand)

        if len(self.obs["deck"].cards)+num_handcards < 10:
            payoffs = np.array([1.0 for i in range(self.player_num)])


        else:
            payoffs = np.array([score / 98 for i in range(self.player_num)])

        return payoffs

    def get_state(self,player_id):
        ''' Get the state given player id
        Args:
            player_id (int): The player id
        Returns:
            (numpy.array): The observed state of the player
        '''

        p_obs = {'deck':self.obs['deck'], 'player': self.players[player_id], 'others': np.delete(self.players,player_id)}
        return self._extract_state(p_obs)

    def get_perfect_information(self):
        ''' Get the perfect information of the current state
        Returns:
            (dict): A dictionary of all the perfect information of the current state
        Note: Must be implemented in the child class.
        '''

        return [p for p in self.players if p != self.current_player]

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return seed

    def _init_game(self):
        ''' Start a new game
        Returns:
            (tuple): Tuple containing:
                (numpy.array): The begining state of the game
                (int): The begining player
        '''

        deck = Deck()
        deck.shuffle()


        # name = names.get_first_name()

        self.players = [Player(num)
                        for num in range(self.player_num)]

        for p in self.players:
            p.draw_hand(deck, self.player_num)

        self.current_player = self.players[random.randint(0, self.player_num - 1)]

        if self.state_shape == [5,100]:
            state = {'player': self.current_player, 'deck': deck,'others': None}
        else:
            state = {'player': self.current_player, 'deck': deck,'others': [p for p in self.players if p != self.current_player]}

        self.obs = state

        if self.record_action:
            self.action_recorder=[]
        return self._extract_state(self.obs), self.current_player.id

    def _extract_state(self, obs):
        ''' Extract useful information from state for RL. Must be implemented in the child class.
        Args:
            obs (dict): The perfect obs
        Returns:
            (numpy.array): The extracted state
        '''

        # Hot encoding of the cards in hand:

        player = obs["player"]
        deck = obs["deck"]
        others = obs["others"]
        state = np.zeros(self.state_shape)

        for index in deck.upwardPile[0][1:]:
            state[0][index] = 1

        for index in deck.upwardPile[1][1:]:
            state[1][index] = 1

        for index in deck.downwardPile[0]:
            if index != 100:
                state[2][index] = 1

        for index in deck.downwardPile[1]:
            if index != 100:
                state[3][index] = 1
        for index in player.hand:
            if index != -1:
                state[4][index] = 1

        if self.strategy == "ideal":
            i=0
            for p in others:
                for index in p.hand:
                    if index != -1:
                        state[5+i][index] = 1
                i=i+1
        return state

    def get_legal_actions(self):

        return self._get_legal_actions()

    def _get_legal_actions(self, ):
        ''' Get all legal actions for current state.
        Returns:
            (list): A list of legal actions' id.
        Note: Must be implemented in the child class.
        '''

        deck = self.obs["deck"]
        player =self.obs["player"]

        legal = []


        if player.give_hint==True:
            legal = [1,101,201,301]

            return legal

        if player.num_played_cards == 5:
            legal.append(0)

            return legal


        if player.num_played_cards >= 2 or (deck.is_deck_empty() == True and player.num_played_cards == 1):
            legal.append(0)


        else:
            for index, card in enumerate(player.hand):
                if (card > deck.upwardPile[0][len(deck.upwardPile[0]) - 1] or card == deck.upwardPile[0][len(deck.upwardPile[0]) - 1] - 10) and card != -1:
                    legal.append(card)
                if ((card > deck.upwardPile[1][len(deck.upwardPile[1]) - 1]) or (
                        card == deck.upwardPile[1][len(deck.upwardPile[1]) - 1] - 10)) and card != -1:
                    legal.append(card + 100)

                if ((card < deck.downwardPile[0][len(deck.downwardPile[0]) - 1]) or (
                        card == deck.downwardPile[0][len(deck.downwardPile[0]) - 1] + 10)) and card != -1:
                    legal.append(card + 200)

                if ((card < deck.downwardPile[1][len(deck.downwardPile[1]) - 1]) or (
                        card == deck.downwardPile[1][len(deck.downwardPile[1]) - 1] + 10)) and card != -1:
                    legal.append(card + 300)

        return legal

    @staticmethod
    def init_game():
        ''' (This function has been replaced by `reset()`)
        '''
        raise ValueError('init_game is removed. Please use env.reset()')
