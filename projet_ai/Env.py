from projet_ai import Event, Player, Car, Map, Settings, Game
import pygame


class Env:
	def __init__(self, name='Taxi Agent Editor', use_ai=False, map_name=None):
		self.name = name
		self.map_name = map_name
		self.use_ai = use_ai

		pygame.init()

		self.evManager = Event.EventManager()

		if self.name == 'Taxi Agent':
			self.player = Player.Player(self.evManager)

			self.character = Car.Car(Settings.CAR_IMAGE, self.evManager)
			self.map = Map.Map(self.evManager)

			if self.map_name is not None:
				self.map.load_map(self.map_name)
				self.mode = Game.Mode(Game.Mode.PLAY_MODE)
			else:
				self.mode = Game.Mode(Game.Mode.POINT_EDITING)

			self.game = Game.Game(self.player, self.character, self.map, self.mode, self.evManager)
			self.gameController = Game.GameController(self.game, self.evManager)

			self.gameView = None

			self.evManager.post(Event.ChangeModeEvent(self.mode))

	def __del__(self):
		pygame.quit()

	def reset(self):
		self.gameController.reset()
		self.game.start()
		return self.character.get_state()

	def get_number_inputs(self):
		return self.character.get_number_inputs()

	def run(self):
		self.gameView = Game.GameView(self.game, self.gameController, self.evManager, True)
		self.gameController.start()
		self.gameController.run()

	def step(self, action):
		if not self.gameController.as_started():
			self.gameController.start()
		return self.gameController.step(action)

	def render(self):
		if self.gameView is None:
			self.gameView = Game.GameView(self.game, self.gameController, self.evManager)
		self.gameView.render()
