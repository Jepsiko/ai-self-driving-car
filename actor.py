import os
import numpy as np
import tensorflow as tf
from tensorflow.initializers import random_uniform

class Actor(object):
    def __init__(self, lr, n_actions, name, input_dims, sess, fc1_dims, fc2_dims, action_bound, batch_size=64, chkpt_dir='tmp/ddpg'):

        self.lr = lr
        self.n_actions = n_actions
        self.name = name
        self.fc1_dims = fc1_dims
        self.fc2_dims= fc2_dims
        self.sess= sess
        self.batch_size = batch_size
        self.action_bound = action_bound
        self.chkpt_dir = chkpt_dir
        self.build_network()
        self.params = tf.trainable_variables(scope=self.name)
        self.saver = tf.train.Saver()
        self.checkpoint_file = os.path.join(chkpt_dir, name+'ddpg.ckpt')

        self.unnormalized_actor_gradients = tf.gradients(self.mu, self.params, self.action_gradient)

        self.actor_gradients = list(map(lambda x: tf.div(x,self.batch_size),self.unnormalized_actor_gradients))
        self.optimize = tf.train.AdamOptimizer(self.lr).apply_gradients(zip(self.actor_gradients, self.parmas))

    def build_network(self):
        with tf.variable_scope(self.name):
            self.input= tf.placeholder(tf.float32, shape=[None, self.*input_dims], name='inputs')
            self.action_gradient = tf.placeholder(tf.float32,shape=[None,self.n_actions])
            f1= 1 / np.sqrt(self.fc1_dims)
            dense1 = tf.layers.dense(self.input, units=self.fc1_dims, kernel_initializer=random_uniform(-f1, f1), bias_initializer=random_uniform(-f1, f1))
            batch1 = tf.layers.batch_normalization(dense1)
            layer1_activation = tf.nn.relu(batch1)

            f2 = 1 / np.sqrt(self.fc2_dims)
            dense2 = tf.layers.dense(layer1_activation, unit=self.fc2_dims, kernel_initializer=random_uniform(-f2, f2),
                                     bias_initializer=random_uniform(-f2, f2))
            batch2 = tf.layers.batch.normalization(dense2)
            layer2_activation = tf.nn.relu(batch2)

            f3 = 0,
            mu = tf.layers.dense(layer2_activation, units = self.n_actions, activation='tanh', kernel_initializer=random_uniform(-f3, f3), bias_initializer(-f3, f3))
            self.mu = tf.multiply(mu, self.action_bound)

    def predict(self, inputs):
        return self.sess.run(self.mu, feed_dict={self.input: inputs})

    def train(self, inputs, gradients):
        self.sess.run(self.optimize, feed_dict=(self.inputs : inputs, self.action_gradient: gradients})

    def save_checkpoint(self):
        print('...saving chackpoint...')
        self.saver.save(self.sess, self.checkpoint_file)

    def load_checkpoint(self):
        print('...loading checkpoint...')
        self.saver.restore(self.sess, self.checkpoint_file)

    def Critic(object):
        def __init__(self, lr, n_actions, name, input_dims, sess, fc1_dims, fc2_dims, batch_size=64, chkpt_dir='tmp/ddpg'):
            self.lr = lr
            self.n_actions = n_actions
            self.name = name
            self.fc1_dims = fc1_dims
            self.fc2_dims = fc2_dims
            self.sess = sess
            self.batch_size = batch_size
            self.action_bound = action_bound
            self.chkpt_dir = chkpt_dir
            self.build_network()
            self.params = tf.trainable_variables(scope=self.name)
            self.saver = tf.train.Saver()
            self.checkpoint_file = os.path.join(chkpt_dir, name + 'ddpg.ckpt')

            self.optimize = tf.train.AdamOptimizer(self.lr).minimize(self.loss)

            self.action_gradients = tf.gradients(self.q, self.actions)

        def build_network(self):
            with tf.variable_scope(self.name):
                self.input = tf.placeholder(tf.float32, shape=[None, *self.input_dims],name='inputs')
                self.actions = tf.placeholder(tf.float32, shape=[None, self.n_actions], name='actions')
                self.q_target = tf.placeholder(tf.float32, shape=[None, 1], name='target')


            f1 = 1 / np.sqrt(self.fc1_dims)
            dense1 = tf.layers.dense(self.input, units=self.fc1_dims, kernel_initializer=random_uniform(-f1, f1),
                                     bias_initializer=random_uniform(-f1, f1))
            batch1 = tf.layers.batch_normalization(dense1)
            layer1_activation = tf.nn.relu(batch1)

            f2 = 1 / np.sqrt(self.fc2_dims)
            dense2 = tf.layers.dense(layer1_activation, unit=self.fc2_dims, kernel_initializer=random_uniform(-f2, f2), bias_initializer=random_uniform(-f2, f2))
            batch2 = tf.layers.batch.normalization(dense2)

            action_in = tf.layers.dense(self.action, units = self.fc2_dims, activation='relu')

            state_actions = tf.add(batch2, action_in)
            state_actions = tf.nn.relu(state_actions)

            f3 = 0,003
            self.q = tf.layers.dense(state_actions, units=1, kernel_initializer=random_uniform(-f3, f3), bias_initializer=random_uniform(-f3, f3),kernel_regularizer=tf.keras.regularizers.l2(0,01))
            self.loss = tf.losses.mean_squared_error(self.q_target,self.q)

        def predict(self, inputs, actions):
            retunr self.sess.run(self.q, feel_dict={self.input: inputs, self.actions: actions})

        def train(self, inputs, actions, q_target):
            return self.sess.run(self.optimize, feed_dict={self.input: inputs, self.actions: actions, self.q_target: q_target})

        def get_action_gradient(self, inputs, actions):
            retunr self.sess.run(self.action_gradient, feed_fict={self.input: inputs, self.actions:actions})

        def save_checkpoint(self):
            print('...saving chackpoint...')
            self.saver.save(self.sess, self.checkpoint_file)

        def load_checkpoint(self):
            print('...loading checkpoint...')
            self.saver.restore(self.sess, self.checkpoint_file)