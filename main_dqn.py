''' An example of learning a Deep-Q Agent on Dou Dizhu
'''

import tensorflow as tf
import os

from agents.DQNAgent import DQNAgent
from rlcard.envs.registration import DEFAULT_CONFIG
from rlcard.utils import tournament, set_global_seed
from rlcard.utils import Logger

from game.environment import Env






# Make environment
_config = DEFAULT_CONFIG.copy()

_config['seed']=0
_config['active_player']= 0
_config['number_players']= 2
_config['state_shape']= [5,100]
_config['number_actions']=400

_config['single_player_mode']=False

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
set_global_seed(0)
#tf.compat.v1.set_random_seed(0)


with tf.compat.v1.Session() as sess:
    # Initialize a global step
    global_step = tf.Variable(0, name='global_step', trainable=False)

    # Set up the agents
    agents=[]

    for i in range(env.number_players):

        agent = DQNAgent(sess,
                         scope='dqn'+str(i),
                         number_actions=env.number_actions,
                         replay_memory_init_size=memory_init_size,
                         train_every=train_every,
                         state_shape=env.state_shape,
                         mlp_layers=[50, 40])

        agents.append(agent)

    env.set_agents(agents)

    eval_env.set_agents(agents)


    # Initialize global variables
    sess.run(tf.compat.v1.global_variables_initializer())

    # Init a Logger to plot the learning curve
    logger = Logger(log_dir)




    #Load model
    #saver = tf.train.import_meta_graph('models/theGame_dqn/model.data-00000-of-00001')
    #saver.restore(sess, tf.train.latest_checkpoint('models/theGame_dqn'))

    for episode in range(episode_num):
        print("episode {}".format(episode))
        # Generate data from the environment
        trajectories, _ = env.run(is_training=True)

        # Feed transitions into agent memory, and train the agent

        for i in range(env.number_players):
            for ts in trajectories[i]:
                agents[i].feed(ts)

        # Evaluate the performance. Play with random agents.
        if episode % evaluate_every == 0:
            logger.log_performance(env.timestep, tournament(eval_env, evaluate_num)[0])


    # Close files in the logger
    logger.close_files()

    # Plot the learning curve
    logger.plot('DQN')

    # Save model
    save_dir = 'models/theGame_dqn_2P'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    saver = tf.train.Saver()
    saver.save(sess, os.path.join(save_dir, 'models'))

