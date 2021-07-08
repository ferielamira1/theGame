theGame
For the implementation, Python 3.7 with Tensorflow 1.15.4 were used. The code is based on the core of RLCard , which is a toolkit for reinforcement learning in card games. Three types of agents were integrated: random, heuristic and a DQN-agent. The two first models serve to evaluate the DQN algorithm.

#The Game

Our system structure is relatively simple.

The "Game" folder contains a "Player "class, which contains information about the respective players and "Deck" class, which contains information about the common deck between all players.
"main_dqn.py" is the controller, for the DQN agent, takes three arguments: Integer: number of players, String: strategy name, Bool: Training
"environment.py" contains the "Environment" class and represents interaction point between the agents and the game.
"dqn_agent.py" contains the DQN agent.
The utility functions are encapsulated in "utils.py". Figure 6, details the life cycle of training an agent.
The strategies are:

Independent strategy ("non-communicative") Each player knows their hand cards, the cards previously played on the pile, the cards on the top of the pile and there is no established communication.

Informed strategy ("h_informative")Each player knows their hand cards, the cards previously played on the pile and the cards on the top of the pile. Moreover, the players use a pre-defined communication protocol: For each co-player j and each of the 4 piles P_i: If the co-player can use the backward trick on P_i or has a playable card which distance to the top of the pile P_i is smaller than two, then, a hint H_(i,j) gets sent to the co-players. In this case, the agent only learns to interpret a communication message but not to send one.

Informative strategy ("informative") Each player knows their hand cards, the cards previously played on the pile and the cards on the top of the pile. Moreover, players learn how to communicate by sending each other hints and interpreting them. The players use one of the following hints: Do not play on the first ascending pile. Do not play on the second ascending pile. Do not play on the first descending pile. Do not play on the second descending pile.

Cheated stratgy ("ideal"):Each player knows their hand cards, the cards previously played on the pile and the cards on the top of the pile. Moreover, players cheat by peaking at their coplayers cards

DQN architecture: Architecture The input layer represents the valuable observations of the agent, independently from which strategy is used, an input of 100×5 has been opted for, representing the observations of the agent: the four visible piles and the cards in the player's hand. In the case of the independent strategy, the hints are always set to zero and are seen as dummy cells. the output layer gives back the 400 different Q-Values corresponding to the actions

Furthermore, our network is comprised of two hidden layers of size 512-512, with tanh activation function. The DQN agent uses experience replay, with a memory size bounded between 1000 and 50000 and batches of size 32, drawn randomly from the pool of stored samples. The discount factor is set to 0.99. The main model will be trained after each game with an Adam optimizer and a learning rate of 〖5.10〗^(-5), and the target model will be updated every 1000 games. An ε-greedy exploration policy is used, making the algorithm off-policy. Furthermore, the algorithm uses squared-rror loss over the mean of the training samples to optimize the DQN model. The metric used as a measurment of quality, is the average amount of rewards collected over a certain number of games. This has been chosen since the loss function isn't a good performance indicator in reinforcement learning. [10] Cell Meaning
