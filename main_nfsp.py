"""
Copyright (c) 2019 DATA Lab at Texas A&M University

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
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
import sys
from datetime import date

import tensorflow as tf
import os

from agents.NFSPAgent import NFSPAgent
from agents.RandAgent import RandomAgent
from utils import set_global_seed, tournament
from rlcard.utils import Logger
from environment import Env
from rlcard.envs.registration import DEFAULT_CONFIG




# Make environment

'''
Read the argumets
1. Number of players: 1-5
2. Strategy: random - non-communicative - ideal 
3. Training: True - False
'''

player_num = int(sys.argv[1])
strategy = str(sys.argv[2])
training = bool(sys.argv[3])


# Make environment
_config = DEFAULT_CONFIG.copy()

_config['seed']=0
_config['active_player']= 0
_config['player_num']= player_num


if strategy=="ideal":
    _config['state_shape']= [4+player_num,100]
else:
    _config['state_shape']= [5,100]

_config['strategy']=strategy # POSSIBLE STRATEGY TYPES: H_INFORMATIVE,  INFORMATIVE, IDEAL, NONE

_config['number_actions']=400
_config['record_action']=True
_config['heuristic_communication']=False

env = Env(_config)
eval_env = Env(_config)

# Set the iterations numbers and how frequently we evaluate the performance
evaluate_every = 100
evaluate_num = 1000
episode_num = 10

# The intial memory size
memory_init_size = 1000

# Train the agent every X steps
train_every = 1

log_dir = './experiments/theGame_nfsp_result/'

# Set a global seed
set_global_seed(0)

with tf.Session() as sess:
    # Initialize a global step
    global_step = tf.Variable(0, name='global_step', trainable=False)

    # Set up the agents
    agents = []
    random_angents=[]
    for i in range(env.player_num):
        agent = NFSPAgent(sess,
                          scope='nfsp' + str(i),
                          action_num=env.number_actions,
                          train_every=train_every,
                          state_shape=env.state_shape,
                          mlp_layers=[512, 512])
        agents.append(agent)

        #random_agent = RandomAgent(action_num=eval_env.number_actions)
        #random_angents.append(random_agent)

    env.set_agents(agents)
    eval_env.set_agents(agents)

    # Initialize global variables
    sess.run(tf.global_variables_initializer())

    # Init a Logger to plot the learning curvefrom rlcard.agents.random_agent import RandomAgent

    logger = Logger(log_dir)
    #saver = tf.train.import_meta_graph('./models/theGame_nfsp/model.data-00000-of-00001')
    #saver.restore(sess, tf.train.latest_checkpoint('./models/theGame_nfsp'))

    for episode in range(episode_num):

        # First sample a policy for the episode
        for agent in agents:
            agent.sample_episode_policy()

        # Generate data from the environment
        trajectories, _ = env.run(is_training=True)

        # Feed transitions into agent memory, and train the agent
        for i in range(env.player_num):
            for ts in trajectories[i]:
                agents[i].feed(ts)

        # Evaluate the performance. Play with random agents.
        if episode % evaluate_every == 0:
            performance = tournament(eval_env, evaluate_num)

            logger.log_performance(episode, performance[0])
    # Close files in the logger
    logger.close_files()

    # Plot the learning curve
    #logger.plot('NFSP')

    # Save model
    today = date.today()
    d = today.strftime("%b_%d_%Y")
    save_dir = 'models/nfsp/'+strategy+str(player_num)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    saver = tf.train.Saver()
    saver.save(sess, os.path.join(save_dir, 'model'))

