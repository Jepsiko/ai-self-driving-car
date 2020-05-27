from projet_ai import Agent, Env
import numpy as np


def main():
	env = Env.Env('Taxi Agent Editor', use_ai=True, map_name='map2')

	agent = Agent.Agent(alpha=0.0001, beta=0.001, input_dims=[env.get_number_inputs()], tau=0.0005, env=env, batch_size=64, layer1_size=800,
						layer2_size=300, n_actions=2)
	score_history = []
	mean_history = []
	np.random.seed(0)

	for i in range(1000):

		obs = env.reset()
		done = False
		score = 0

		while not done:
			# print('\n------------- State  -------------')
			# print(obs)
			action = agent.choose_action(obs)
			# print('\n------------- Action -------------')
			# print(action)

			new_state, reward, done, info = env.step(action)

			agent.remember(obs, action, reward, new_state, int(done))
			agent.learn()

			score += reward
			obs = new_state

		score_history.append(score)
		mean = np.mean(score_history[-100:])
		mean_history.append(mean)
		print("episode ", i, 'score %.2f' % score, '100 game average %.2f' % mean)


if __name__ == "__main__":
	main()
