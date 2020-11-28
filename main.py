import random

import names

from DQN import DQNAgent
from Player import Player
from Deck import Deck
import numpy as np
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import statistics

from keras.utils import to_categorical


actions = ["upwardsPile1","upwardsPile2","downwardsPile1","downwardsPile2"]

def define_parameters():
    params = dict()
    # Neural Network
    params['epsilon_decay_linear'] = 1/75
    params['learning_rate'] = 0.0005
    params['first_layer_size'] = 50   # neurons in the first layer
    params['second_layer_size'] = 300   # neurons in the second layer
    params['third_layer_size'] = 50    # neurons in the third layer
    params['episodes'] = 150
    params['memory_size'] = 2500
    params['batch_size'] = 1000
    # Settings
    params['weights_path'] = 'weights/weights3'
    params['load_weights'] = False
    params['train'] = True
    params['plot_score'] = False
    return params

def plot_seaborn(array_counter, array_score,train):
    sns.set(color_codes=True, font_scale=1.5)
    sns.set_style("white")
    plt.figure(figsize=(13,8))
    if train==False:
        fit_reg = False
    ax = sns.regplot(
        np.array([array_counter])[0],
        np.array([array_score])[0],
        #color="#36688D",
        x_jitter=.1,
        scatter_kws={"color": "#36688D"},
        label='Data',
        fit_reg = fit_reg,
        line_kws={"color": "#F49F05"}
    )
    # Plot the average line
    y_mean = [np.mean(array_score)]*len(array_counter)
    ax.plot(array_counter,y_mean, label='Mean', linestyle='--')
    ax.legend(loc='upper right')
    ax.set(xlabel='# games', ylabel='score')
    plt.ylim(0,65)
    plt.show()




def test(params):
    params['load_weights'] = True
    params['train'] = False
    score, mean, stdev = run(params)
    return score, mean, stdev




# def initialize_game(player, deck, agent, batch_size):
#     state_init1 = agent.get_state(player.hand, deck.upwardPile[0], deck.upwardPile[1],deck.downwardPile[0],deck.downwardPile[1])
#     action = 1
#     player.action(deck,player.hand,action)
#
#     state_init2 = agent.get_state(player.hand, deck.upwardPile[0], deck.upwardPile[1],deck.downwardPile[0],deck.downwardPile[1])
#
#     reward1 = agent.set_reward(player, game.crash)
#     agent.remember(state_init1, action, reward1, state_init2, game.crash)
#     agent.replay_new(agent.memory, batch_size)



def run(params):
    score_plot = []
    counter_plot = []
    record = 0
    total_score = 0

    agent = DQNAgent()

    if len(sys.argv) < 2:
        raise ValueError("You need to set the number of players.")
    else:
        if ((not str.isdigit(sys.argv[1])) or (not (int(sys.argv[1]) in range(-1, 6)))):
            raise ValueError("You need to set the number of players between 1-5")


    counter_games = 0

    while counter_games < params['episodes']:
        gameOver = False
        game_score = 0

        # initializing
        deck = Deck()
        deck.shuffle()

        name = names.get_first_name()
        player = Player(name)
        player.drawHand(deck, 1)
        player.showHand()

        # initializeGame()

        while not gameOver:

            if not params['train']:
                agent.epsilon = 0.00
            else:
                print("Training episode {} ... ".format(counter_games))
                # agent.epsilon is set to give randomness to actions
                agent.epsilon = 1 - (counter_games * params['epsilon_decay_linear'])

            state_old = agent.get_state(player.hand, deck.upwardPile[0], deck.upwardPile[1], deck.downwardPile[0],
                                        deck.downwardPile[1])

            # perform random actions based on agent.epsilon, or choose the action
            if random.uniform(0, 1) < agent.epsilon:
                final_move = to_categorical(random.randint(0, 3), num_classes=4)
                print("Executing random action ... ")
            else:
                # predict action based on the old state
                prediction = agent.model.predict(state_old)
                final_move = to_categorical(np.argmax(prediction[0]), num_classes=4)
                print("Executing predicted action ... ")


            # perform new move and get new state
            reward = player.action(deck, player.hand, final_move)
            if reward:
                if deck.isDeckEmpty() and len(player.hand)==0:
                    gameOver=True
                    game_score = game_score  + 10
                else:
                    game_score = game_score +1
            else:
                game_score = game_score  -10
                gameOver=True


            state_new = agent.get_state(player.hand, deck.upwardPile[0], deck.upwardPile[1], deck.downwardPile[0],
                                        deck.downwardPile[1])
            print("CURRENT STATE {}".format(state_new))

            reward = agent.set_reward(reward)
            if params['train']:
                # train short memory base on the new action and state
                print("Training short term memory ... ")
                agent.train_short_memory(state_old, final_move, reward, state_new, reward)
                # store the new data into a long term memory
                print("Storing the data ... ")
                agent.remember(state_old, final_move, reward, state_new, reward)

                agent.replay_new(agent.memory, params['batch_size'])
        counter_games += 1
        total_score = +  game_score
        score_plot.append(game_score)
        counter_plot.append(counter_games)

        print("GAME SCORE: {}".format(game_score))
    mean, stdev = statistics.mean(score_plot), statistics.stdev(score_plot)


    if params['train']:
        agent.model.save_weights(params['weights_path'])
        total_score, mean, stdev = test(params)
    if params['plot_score']:
        plot_seaborn(counter_plot, score_plot, params['train'])
    print('Total score: {}   Mean: {}   Std dev:   {}'.format(total_score, mean, stdev))
    return total_score, mean, stdev

if __name__ == '__main__':
    params = define_parameters()


    run(params)





            #########################################################################
    ###########################OLD IMPLEMENTATION############################
    #########################################################################
    #
    # if len(sys.argv) <2 :
    #     raise ValueError("You need to set the number of players.")
    # else:
    #     if ( (not str.isdigit(sys.argv[1])) or (not (int(sys.argv[1])in range(-1,6)))):
    #         raise ValueError("You need to set the number of players between 1-5")
    #
    #     deck = Deck()
    #     deck.shuffle()
    #
    #     numberPlayers = int(sys.argv[1])  #int(input("Enter a number of players between 1-5: \n"))
    #     players = []
    #
    #     for i in range(1,numberPlayers+1):
    #         name = names.get_first_name()
    #         p = Player(name)
    #         p.drawHand(deck, numberPlayers)
    #         p.showHand()
    #         players.append(p)
    #
    #     agent = DQNAgent()
    #
    #     model = agent.network()
    #     y = model(getState(players[0].hand,deck.upwardPile[0],deck.upwardPile[1],deck.downwardPile[0],deck.downwardPile[1]))
    #     gameOver = False
    #
    #     while(gameOver==False):
    #         for player in players:
    #             mustPlay = True
    #             stillPlaying=True
    #             numberLayedCards=0
    #
    #             while(gameOver == False
    #                   and(stillPlaying == True
    #                   or mustPlay == True)):
    #
    #                 print("The next player is {} \n".format(player.name))
    #
    #                 #check if hand contains a card that is smaller than downwards  or bigger than  upwards
    #
    #                 if (not (numberLayedCards < 2 and len(deck.cards) > 0) or (
    #                         numberLayedCards < 1 and len(deck.cards) == 0)):
    #                     mustPlay = False
    #                     print("Player can stop")
    #
    #
    #                 if (mustPlay and (all( (card > deck.downwardPile[0]for card in player.hand))
    #                                   and all(card > deck.downwardPile[1] for card in player.hand)
    #                                   and all(card < deck.upwardPile[0] for card in player.hand)
    #                                   and all(card < deck.upwardPile[1] for card in player.hand)
    #                                   and all(card != deck.downwardPile[0] +10 for card in player.hand)
    #                                   and all(card != deck.downwardPile[1] +10 for card in player.hand)
    #                                   and all(card != deck.upwardPile[0] -10 for card in player.hand)
    #                                   and all(card != deck.upwardPile[1] -10 for card in player.hand))):
    #                     gameOver = True
    #                     break
    #
    #                 player.showHand()
    #
    #                 print("The stacked cards are currently in this state: \n Going UPWARDS: \n "
    #                     "1) \u2191 {} \n 2) \u2191 {} \n "
    #                     "Going DOWNWARDS: \n"
    #                     "3) \u2193 {} \n 4) \u2193 {} \n".format(deck.upwardPile[0],deck.upwardPile[1],deck.downwardPile[0],deck.downwardPile[1]))
    #
    #                 card = deck.computeDistance(player.hand)
    #
    #                 result = player.play(deck,player.hand)
    #
    #                 if result:
    #                     numberLayedCards += 1
    #
    #                 if not result:
    #                     stillPlaying = False
    #                     if (numberLayedCards<2 and deck.isDeckEmpty()==False) or (numberLayedCards<1 and deck.isDeckEmpty()==True):
    #                         gameOver = True
    #                         break
    #
    #                 if numberPlayers == 1:
    #                     drawnCard = player.drawCard(deck)
    #                     print("You've drawn the card {} \n".format(drawnCard))
    #
    #
    #                 elif numberLayedCards>2 :
    #                     if stillPlaying==False:
    #                         for _ in range(numberLayedCards):
    #                             if not deck.isDeckEmpty():
    #                                 drawnCard = player.drawCard(deck)
    #                                 print("You've drawn the card {}".format(drawnCard))
    #
    #     totalCards = 0
    #     for player in players:
    #         totalCards += len(player.hand)
    #     if totalCards + len(deck.cards) <=10:
    #
    #         print("CONGRATULATIONS,YOU HAVE AN EXCELLENT SCORE!")
    #     else:
    #         print("YOU DIED WITH SCORE: {}".format(totalCards + len(deck.cards)))
    #
    #
    #
    #





