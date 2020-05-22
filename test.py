import Agent
import gym
import numpy as np
# from utils import plotLearning


if __name__ == "__main__":
	using_ai = True
	env = gym.make("Pendulum-v0")
	agent = Agent.Agent(alpha=0.0001, beta=0.001, input_dims=[3], tau=0.001, env=env, batch_size=64, layer1_size=400,
						layer2_size=300, n_actions=1)
	score_history = []
	np.random.seed(0)
	for i in range(1000):
		state = env.reset()
		done = False
		score = 0
		while not done:
			if using_ai:
				action = agent.choose_action(state)
			else:
				action = float(input("action : "))
			new_state, reward, done, info = env.step(action)
			if using_ai:
				agent.remember(state, action, reward, new_state, int(done))
				agent.learn()
			score += reward
			state = new_state
		score_history.append(score)
		print("episode ", i, 'score %.2f' % score, '100 game average %.2f' % np.mean(score_history[-100:]))

	# filename = 'pendulum.png'
	# plotLearning(score_history, filename, window=100)