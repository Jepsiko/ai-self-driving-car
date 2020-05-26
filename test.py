from projet_ai import Agent
import gym
import numpy as np
# from utils import plotLearning
import matplotlib.pyplot as pl


if __name__ == '__main__':
	using_ai = True
	env = gym.make('Pendulum-v0')
	print(env.action_space.high)
	agent = Agent.Agent(alpha=0.0001, beta=0.001, input_dims=[3], tau=0.0005, env=env, batch_size=64, layer1_size=800,
                        layer2_size=300, n_actions=1)
	score_history = []
	mean_history = []
	np.random.seed(0)
	for i in range(1000):
		obs = env.reset()
		done = False
		score = 0
		while not done:
			if using_ai:
				action = agent.choose_action(obs)
			else:
				action = float(input("action : "))

			new_state, reward, done, info = env.step(action)

			if using_ai:
				agent.remember(obs, action, reward, new_state, int(done))
				agent.learn()

			score += reward
			obs = new_state
		score_history.append(score)
		mean = np.mean(score_history[-100:])
		mean_history.append(mean)
		print("episode ", i, 'score %.2f' % score, '100 game average %.2f' % mean)

	pl.plot(score_history)
	pl.plot(mean_history)
	pl.show()

	# filename = 'pendulum.png'
	# plotLearning(score_history, filename, window=100)