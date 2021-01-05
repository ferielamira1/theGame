''' An example of learning a Deep-Q Agent on Dou Dizhu
'''

import tensorflow as tf
import os

import rlcard
from DQN_RLCard_v2 import DQNAgent
from rlcard.agents import RandomAgent
from rlcard.envs.registration import DEFAULT_CONFIG
from rlcard.utils import set_global_seed, tournament
from rlcard.utils import Logger

from environment import Env

# Make environment
_config = DEFAULT_CONFIG.copy()

_config['seed']=0
_config['active_player']=1

env = Env(_config)
eval_env = Env(_config)

# Set the iterations numbers and how frequently we evaluate the performance
evaluate_every = 100
evaluate_num = 1000
episode_num = 100000

# The intial memory size
memory_init_size = 1000

# Train the agent every X steps
train_every = 1

# The paths for saving the logs and learning curves
log_dir = './experiments/dqn_result/'

# Set a global seed

tf.compat.v1.set_random_seed(0)
with tf.compat.v1.Session() as sess:
    # Initialize a global step
    global_step = tf.Variable(0, name='global_step', trainable=False)

    saver = tf.train.Saver()
    agent = saver.restore(sess, 'models/theGame_dqn/model')
    # Set up the agents
    agent = DQNAgent(sess,
                     scope='dqn',
                     action_num=env.action_num,
                     replay_memory_init_size=memory_init_size,
                     train_every=train_every,
                     state_shape=env.state_shape,
                     mlp_layers=[512, 512])
    env.set_agents([agent])
    eval_env.set_agents([agent])

    # Initialize global variables
    sess.run(tf.compat.v1.global_variables_initializer())

    # Init a Logger to plot the learning curve
    logger = Logger(log_dir)

    for episode in range(episode_num):
        print("episode {}".format(episode))
        # Generate data from the environment
        trajectories, _ = env.run(is_training=True)

        # Feed transitions into agent memory, and train the agent

        for ts in trajectories[0]:
            agent.feed(ts)

        # Evaluate the performance. Play with random agents.
        if episode % evaluate_every == 0:
            logger.log_performance(env.timestep, tournament(eval_env, evaluate_num)[0])


    # Close files in the logger
    logger.close_files()

    # Plot the learning curve
    logger.plot('DQN')

    # Save model
    save_dir = 'models/theGame_dqn'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    saver = tf.train.Saver()
    saver.save(sess, os.path.join(save_dir, 'model'))

