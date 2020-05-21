import tensorflow as tf


class Agent:

	def __init__(self, lidar):
		self.input_size = lidar.row * lidar.col + 2
		self.output_size = 2

# Need a replay buffer class
# Need a class for a target Q network (function of s, a)
# We will use batch norm
# The policy is deterministic, how to handle explore exploit?
# Deterministic policy means outputs the action instead of the probability
# Will need a way to bound the actions to the env limits
# We have two actor and two critic networks, a target for each.
# Updates are soft, according to theta_prime = tau*theta + (1-tau)*theta_prime, with tau << 1
# The target actor is just the evaluation actor plus some noise process
# They used Ornstein Uhlenbeck, (will need to look that up) -> will need a class for noise
