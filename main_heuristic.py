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
import csv

import tensorflow as tf
import os

from agents.DQNAgent import DQNAgent
from agents.HeursiticAgent import HeuristicAgent
from rlcard.envs.registration import DEFAULT_CONFIG
from rlcard.utils import tournament, set_global_seed
from rlcard.utils import Logger

from environment_informative import Env
import sys
from datetime import date



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

if strategy == "non-communicative":
    _config['strategy']="non-communicative"
    _config['state_shape']= [5,100]

if strategy=="ideal":
    _config['strategy']="ideal"

    _config['state_shape']= [4+player_num,100]

if strategy =="informative":
    _config['strategy']="informative"
    _config['state_shape']= [5,100]

_config['number_actions']=400
_config['record_action']=True


env = Env(_config)
eval_env = Env(_config)

# Set the iterations numbers and how frequently we evaluate the performance
evaluate_every = 100
evaluate_num = 1000
episode_num = 200000

# The intial memory size
memory_init_size = 1000

# Train the agent every X steps
train_every = 1

# The paths for saving the logs and learning curves
today = date.today()
d = today.strftime("%b_%d_%Y")

log_dir = './experiments/'+strategy+d







# Set up the agents
agents=[]

for i in range(env.player_num):

    agent = HeuristicAgent()

    agents.append(agent)

env.set_agents(agents)

eval_env.set_agents(agents)

# Initialize global variables


# Init a Logger to plot the learning curve
logger = Logger(log_dir)
fpass  = open('passcount.csv', 'w', newline='')
f_highest_performace  = open('highestperformance.csv', 'w', newline='')
performance=[]


#Load model

#saver = tf.train.import_meta_graph('models/theGame_'+str(strategy)+'_dqn_'+str(player_num)+'P_'+'Apr_30_2021'+'/models.data-00000-of-00001')
#saver.restore(sess, tf.train.latest_checkpoint('./models/theGame_'+str(strategy)+'_dqn_'+str(player_num)+'P_'+'Apr_30_2021'))

for episode in range(episode_num):
    #print("episode {}".format(episode))
    # Generate data from the environment

    # Evaluate the performance. Play with random agents.
    print("here")

    if episode % evaluate_every == 0:
        print("now here")

        performance, best_performance, num_pass = tournament(eval_env, evaluate_num)

        logger.log_performance(episode, performance[0])
        writer = csv.DictWriter(fpass, fieldnames=  ['episode', 'number of pass'])

        writer.writerow({'episode': episode, 'number of pass': num_pass})
        print("Average number passes:{}".format(num_pass) )

        writer = csv.DictWriter(f_highest_performace, fieldnames=  ['episode', 'highest performance'])

        writer.writerow({'episode': episode, 'highest performance': best_performance})
        print("Highest performance:{}".format(best_performance) )





# Close files in the logger
logger.close_files()
fpass.close()
f_highest_performace.close()



# Plot the learning curve
logger.plot('Heuristic')



