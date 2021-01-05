import random

import names

from theGame_myImplementation.DQN import DQNAgent
from theGame_myImplementation.Player import Player
from theGame_myImplementation.Deck import Deck
import numpy as np
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import statistics


def plot_seaborn(array_counter, array_score,train):
    sns.set(color_codes=True, font_scale=1.5)
    sns.set_style("white")
    plt.figure(figsize=(13, 8))
    fit_reg = True
    if not train:
        fit_reg = False
    ax = sns.regplot(
        np.array([array_counter])[0],
        np.array([array_score])[0],
        x_jitter=.1,
        scatter_kws={"color": "#36688D"},
        label='Data',
        fit_reg=fit_reg,
        line_kws={"color": "#F49F05"}
    )
    # Plot the average line
    y_mean = [np.mean(array_score)]*len(array_counter)
    ax.plot(array_counter,y_mean, label='Mean', linestyle='--')
    ax.legend(loc='upper right')
    ax.set(xlabel='# games', ylabel='score')
    plt.ylim(0,100)
    plt.show()


if __name__ == '__main__':
    plot_score= True

    score_plot = []
    counter_plot = []
    record = 0
    total_score = 0
    agent = DQNAgent()

    path = agent.weights

    if agent.load_weights:
        agent.model.load_weights(path)
        print("weights loaded.. ")
        print(agent.model.weights)



    if len(sys.argv) < 2:
        raise ValueError("You need to set the number of players.")
    else:
        if (not str.isdigit(sys.argv[1])) or (not (int(sys.argv[1]) in range(-1, 6))):
            raise ValueError("You need to set the number of players between 1-5")
    counter_games = 0

    while counter_games < 2000:


        gameOver = False
        game_score = 0

        # initializing
        deck = Deck()
        deck.shuffle()

        name = names.get_first_name()
        player = Player(name)
        player.draw_hand(deck, 1)


        player.show_hand()

        r_sum=0

        while not gameOver:


            if not agent.train:
                agent.epsilon = 0.00
            else:
                print("Training episode {} ... ".format(counter_games))
                # agent.epsilon is set to give randomness to actions

            state_old = agent.encode_state(player.hand, deck.upwardPile,deck.downwardPile)

            # perform random actions based on agent.epsilon, or choose the action

            played=False
            best = 0
            player.hand =np.array(player.hand)
            reward = -1
            final_move=0
            if random.uniform(0, 1) < agent.epsilon:
                numbers = list(range(0, 32))
                print("Executing random action ... ")
                
                while reward == -1:
                    final_move = random.choice(numbers)
                    numbers.remove(final_move)
                    # perform new move and get new state
                    reward = player.action(deck, final_move)

                print("FINAL ACTION {}:".format(final_move))

                game_score += 1


            else:
                prediction = agent.model.predict(state_old.reshape((1, 12)))
                moves = prediction[0]
                while reward==-1:
                    # predict action based on the old state

                    final_move = np.argmax(moves)
                    moves[final_move]=-1

                    print("Executing predicted action ... ")
                    # perform new move and get new state
                    print("FINAL_MOVE: {}".format(final_move))
                    reward = player.action(deck, final_move)

                game_score+=1

            state_new = agent.encode_state(player.hand, deck.upwardPile, deck.downwardPile)

            print(player.hand)
            print(deck.upwardPile)
            print(deck.downwardPile)

            r_sum = r_sum+reward
            if agent.train:
                # train short memory based on the new action and state
                #print("Training short term memory ... ")
                agent.train_short_memory(state_old, final_move, reward, state_new, gameOver)
                # store the new data into a long term memory
                #print("Storing the data ... ")

                agent.remember(state_old, final_move, reward, state_new, gameOver)

            if not player.can_play(deck):
                gameOver = True
                if game_score> 20:
                    reward=r_sum/98
                else:
                    reward=-1

        if agent.train:
            if len(agent.memory) > agent.batch_size:
                agent.replay_new(agent.memory, agent.batch_size)

        if agent.epsilon > 0.01:
            agent.epsilon=agent.epsilon * agent.epsilon_decay
        counter_games += 1
        total_score = +  game_score
        score_plot.append(game_score)
        counter_plot.append(counter_games)

        print("GAME SCORE: {}".format(game_score))
        print("rewards: {}".format(r_sum))

    mean, stdev = statistics.mean(score_plot), statistics.stdev(score_plot)

    if agent.train:
        agent.model.save_weights(path)
        print("weights saved")

    if plot_score:
        plot_seaborn(counter_plot, score_plot, agent.train)
    print('Total score: {}   Mean: {}   Std dev:   {}'.format(total_score, mean, stdev))




