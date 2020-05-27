from projet_ai import Agent, Env
import numpy as np
import matplotlib.pyplot as plt


def main():
	n_games = int(input('Number of games : '))
	display = input('Display (y/n) ? ') == 'y'

	env = Env.Env('Taxi Agent Editor', use_ai=True, map_name='map2')

	agent = Agent.Agent(alpha=0.0001, beta=0.001, input_dims=[env.get_number_inputs()], tau=0.001, n_actions=2,
						layer1_size=400, layer2_size=300)

	score_history = []
	mean_history = []
	np.random.seed(0)

	if input('Load Agent (y/n) ? ') == 'y':
		agent.load_models()

	for i in range(n_games):

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

			if display:
				env.render()

			agent.remember(obs, action, reward, new_state, int(done))
			agent.learn()

			score += reward
			obs = new_state

		score_history.append(score)
		mean = np.mean(score_history[-100:])
		mean_history.append(mean)
		print("episode ", i, 'score %.2f' % score, '100 game average %.2f' % mean)

	if input('Save Agent (y/n) ? ') == 'y':
		agent.save_models()
	plt.plot(score_history)
	plt.plot(mean_history)
	plt.show()


if __name__ == "__main__":
	main()
