from projet_ai import Agent, Env
import numpy as np
import matplotlib.pyplot as plt


def plot_learning_curve(x, scores, figure_file):
	running_avg = np.zeros(len(scores))
	for i in range(len(running_avg)):
		running_avg[i] = np.mean(scores[max(0, i - 100):(i + 1)])
	plt.plot(x, scores)
	plt.plot(x, running_avg)
	plt.xlabel('Episode')
	plt.ylabel('Score')
	plt.savefig(figure_file)
	plt.show()


def main():
	if input('Enter map editor (y/n) ? ') == 'y':
		env = Env.Env('Taxi Agent')
		env.run()

	else:
		env = Env.Env('Taxi Agent', map_name=input("Map name : "))

		agent = Agent.Agent(alpha=0.0001, beta=0.001, input_dims=[env.get_number_inputs()], tau=0.001, n_actions=2,
							fc1_dims=400, fc2_dims=300)

		score_history = []
		mean_history = []
		np.random.seed(0)
		info = ''
		i = 0

		n_games = int(input('Number of games : '))
		display = input('Display (y/n) ? ') == 'y'

		if input('Load Agent (y/n) ? ') == 'y':
			agent.load_models(input('Agent name : '))

		while info != 'Quit' and i < n_games:

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

				agent.remember(obs, action, reward, new_state, done)
				agent.learn()

				score += reward
				obs = new_state

			score_history.append(score)
			mean = np.mean(score_history[-100:])
			mean_history.append(mean)
			print("episode ", i, 'score %.2f' % score, '100 game average %.2f' % mean)
			i += 1

		if input('Save Agent (y/n) ? ') == 'y':
			agent.save_models(input('Agent name : '))

		for score in score_history:
			print(score)

		# score_history = []
		# file = open('city41_42_chiffre', 'r')
		# for line in file.readlines():
		# 	score_history.append(float(line.strip()))

		x = [i + 1 for i in range(len(score_history))]
		plot_learning_curve(x, score_history, input('Plot file name (.png) : '))


if __name__ == "__main__":
	main()
