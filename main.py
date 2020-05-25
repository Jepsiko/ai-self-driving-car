from projet_ai.Env import Env


def main():
	env = Env('Taxi Agent')
	env.run()
	obs = env.reset()
	done = False
	while not done:
		action = None
		new_state, reward, done, info = env.step(action)
		obs = new_state


if __name__ == "__main__":
	main()
