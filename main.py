import Event
import Game
import GameView


def main():
	evManager = Event.EventManager()

	inputController = Game.InputController(evManager)
	game = Game.Game(evManager)
	gameController = Game.GameController(evManager)
	gameView = GameView.GameView(game, evManager)

	gameController.run()


if __name__ == "__main__":
	main()
