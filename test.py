import Agent
import gym
import numpy as np

if __name__ == "__main__":
	env = gym.make("Pendulum-v0")
	agent = Agent.Agent(alpha=0.0001, beta=0.001, input_dims=[3], tau=0.001, env=env, batch_size=64, layer1_size=400,
						layer2_size=300, n_actions=1)
	score_history = []
	np.random.seed(0)
	for i in range(1000):
		obs = env.reset()
		done = False
		score = 0
		while not done:
			act = agent