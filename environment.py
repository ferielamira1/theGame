from rlcard.utils import *
from game.Player import Player
from game.Deck import Deck
import random
from agents.DQNAgent import DQNAgent


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

                'active_player' (int) - If 'singe_agent_mode' is True,
                 'active_player' specifies the player that does not use
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
        self.active_player = config['active_player']
        self.player_num = config['player_num']
        self.state_shape = config['state_shape']
        self.number_actions = config['number_actions']
        self.current_state = {}
        self.agents: [DQNAgent]
        if self.record_action:
            self.action_recorder = []

        self.timestep = 0
        # Set random seed, default is None
        self._seed(config['seed'])
        self.players = []

    def step(self, action):
        ''' Step forward
        Args:
            action (int): The action taken by the current player
        Returns:
            (tuple): Tuple containing:
                (dict): The next state
                (int): The ID of the next player
        '''

        self.timestep += 1
        # Record the action for human interface
        if self.record_action:
            self.action_recorder.append([self.get_player_id(), action])

        deck = self.current_state["deck"]
        player = self.current_state["player"]

        score = 0

        if action == 0:
            ##print("PLAYER {} DID MOVE {}".format(player.id, action))

            while player.num_played_cards!=0 and not deck.is_deck_empty():

                player.hand[player.hand.index(-1)] = player.draw_card(deck)
                player.num_played_cards = player.num_played_cards - 1
            next_player = self.players[(player.id + 1) % len(self.players)]

            if self.state_shape == [5, 100]:
                next_state = {"player": next_player, "deck": deck, "others": None}
            else:
                next_state = {"player": next_player, "deck": deck, "others": [p for p in self.players if p != next_player]}

            self.current_state = next_state

            #print(self.current_state)
            return self._extract_state(next_state), next_player.id, score


        card = int(action / 4)
        pile = action % 4

        if pile == 0 or pile == 1:
            if ((card > deck.upwardPile[pile][len(deck.upwardPile[pile]) - 1]) or (
                    card == deck.upwardPile[pile][len(deck.upwardPile[pile]) - 1] - 10)) and card != -1:

                deck.upwardPile[pile].append(card)
                player.hand[player.hand.index(card)] = -1

                score += 1

        if pile == 2 or pile == 3:
            if ((card < deck.downwardPile[pile - 2][len(deck.downwardPile[pile - 2]) - 1]) or (
                    card == deck.downwardPile[pile - 2][len(deck.downwardPile[pile - 2]) - 1] + 10)) and card != -1:

                deck.downwardPile[pile - 2].append(card)
                player.hand[player.hand.index(card)] = -1
                score += 1
        if self.state_shape == [5, 100]:
            next_state = {"player": player, "deck": deck, "others": None}
        else:
            next_state = {"player": player, "deck": deck, "others":[p for p in self.players if p != player] }
        player_id = player.id
        player.num_played_cards += 1

        #print("PLAYER {} DID MOVE {}".format(player.id,action))
        self.current_state = next_state
        return self._extract_state(next_state), player_id, score

    def set_agents(self, agents: [DQNAgent]):
        '''
        Set the agents that will interact with the environment.
        This function must be called before `run`.
        Args:
            agents (list): List of Agent classes
        '''
        self.agents = agents


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
        '''

        trajectories = [[] for _ in range(self.player_num)]
        state, player_id = self._init_game()

        # Loop to play the game
        trajectories[player_id].append(state)
        score = 0
        while not self.is_over():
            # Agent plays
            if not is_training:

                action, _ = self.agents[player_id].eval_step(state, self._get_legal_actions())
            else:
                action = self.agents[player_id].step(state, self._get_legal_actions())

            # Environment steps
            next_state, next_player_id, payoff = self.step(action)

            score += payoff

            # Save action
            trajectories[player_id].append(action)

            # Set the state and player
            state = next_state
            player_id = next_player_id
            #print("CURRENT STATE =  player_id: {} , {}".format(
            #    self.current_state["player"].id, next_state ))

            # Save state.
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
        state = self.current_state
        player = state["player"]
        deck = state["deck"]
        if player.can_play(deck):
            return False
        else:
            return True

    def get_player_id(self):
        ''' Get the current player id
        Returns:
            (int): The id of the current player
        '''
        return self.current_state["player"].id


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
        if self.current_state["deck"].is_deck_empty() and len(self.current_state["player"].hand)==0:
            payoffs =  np.array([1.0 for i in range(self.player_num)])
        else:
            payoffs = np.array([score / 98 for i in range(self.player_num)])

        if len(self.current_state["deck"].cards) > 49:

            payoffs = np.array([(score / 98)-1 for i in range(self.player_num)])
        '''
        if self.current_state["deck"].is_deck_empty() and len(self.current_state["player"].hand) == 0:
            payoffs = np.array([1.0 for i in range(self.player_num)])

        else:
            payoffs = np.array([score / 98 for i in range(self.player_num)])

        return payoffs


    def get_state(self, player_id):
        ''' Get the state given player id
        Args:
            player_id (int): The player id
        Returns:
            (numpy.array): The observed state of the player
        '''
        player = self.players[player_id]
        deck = self.current_state["deck"]
        state = {'player': player, 'deck': deck, 'others':None}

        if  self.state_shape!=[5,100]:
            state['others'] = [p for p in self.players if p != self.players[player_id]]

        return self._extract_state(state)


    def get_perfect_information(self):
        ''' Get the perfect information of the current state
        Returns:
            (dict): A dictionary of all the perfect information of the current state
        Note: Must be implemented in the child class.
        '''

        return [p for p in self.players if p != self.active_player]



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
        # deck.cards = [94, 76, 92, 40, 99, 7, 13, 6, 10, 22, 27, 34, 38, 17, 57, 60, 97, 33, 30, 65, 66, 68, 48, 25,
        # 15, 84, 74, 62, 64, 36, 58, 51, 79, 77, 78, 4, 71, 91, 96, 14, 75, 18, 98, 59, 85, 56, 67, 55, 2, 44, 69,
        # 31, 45, 3, 41, 24, 53, 49, 73, 82, 81, 87, 20, 72, 70, 83, 37, 93, 88, 54, 23, 8, 52, 89, 32, 63, 80, 43,
        # 29, 86, 42, 39, 35, 95, 47, 26, 16, 28, 46, 21, 12, 5, 9, 61, 19, 11, 90, 50]

        # name = names.get_first_name()

        self.players = [Player(num)
                        for num in range(self.player_num)]

        for p in self.players:
            p.draw_hand(deck, self.player_num)

        first_player = self.players[random.randint(0, self.player_num - 1)]
        if self.state_shape == [5,100]:
            state = {'player': first_player, 'deck': deck,'others': None}
        else:
            state = {'player': first_player, 'deck': deck,'others': [p for p in self.players if p != first_player]}

        self.current_state = state

        if self.record_action:
            self.action_recorder = []
        return self._extract_state(self.current_state), first_player.id

    def _load_model(self):
        ''' Load pretrained/rule model
        Returns:
            model (Model): A Model object
        '''

    def _extract_state(self, state):
        ''' Extract useful information from state for RL. Must be implemented in the child class.
        Args:
            state (dict): The raw state
        Returns:
            (numpy.array): The extracted state
        '''

        # Hot encoding of the cards in hand:

        player = state["player"]
        deck = state["deck"]
        others = state["others"]
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

        if others!= None:
            i=0
            for p in others:
                for index in p.hand:
                    if index != -1:
                        state[5+i][index] = 1
                i=i+1


        return state

    def get_legal_actions(self):

        return self._get_legal_actions()

    def _get_legal_actions(self):
        ''' Get all legal actions for current state.
        Returns:
            (list): A list of legal actions' id.
        Note: Must be implemented in the child class.
        '''

        player = self.current_state["player"]

        deck = self.current_state["deck"]

        legal = []
        if player.num_played_cards >= 2 or (deck.is_deck_empty() == True and player.num_played_cards == 1):
            legal.append(0)


        for index, card in enumerate(player.hand):
            if (card > deck.upwardPile[0][len(deck.upwardPile[0]) - 1] or card == deck.upwardPile[0][len(deck.upwardPile[0]) - 1] - 10) and card != -1:
                legal.append(card * 4)
            if ((card > deck.upwardPile[1][len(deck.upwardPile[1]) - 1]) or (
                    card == deck.upwardPile[1][len(deck.upwardPile[1]) - 1] - 10)) and card != -1:
                legal.append(card * 4 + 1)

            if ((card < deck.downwardPile[0][len(deck.downwardPile[0]) - 1]) or (
                    card == deck.downwardPile[0][len(deck.downwardPile[0]) - 1] + 10)) and card != -1:
                legal.append(card * 4 + 2)

            if ((card < deck.downwardPile[1][len(deck.downwardPile[1]) - 1]) or (
                    card == deck.downwardPile[1][len(deck.downwardPile[1]) - 1] + 10)) and card != -1:
                legal.append(card * 4 + 3)

        return legal

    @staticmethod
    def init_game():
        ''' (This function has been replaced by `reset()`)
        '''
        raise ValueError('init_game is removed. Please use env.reset()')
