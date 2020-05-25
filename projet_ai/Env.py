from projet_ai import Event, Player, Car, Map, Settings, Game


class Env:
    def __init__(self, name='Taxi Agent Editor', display=True, use_ai=False):
        self.name = name
        self.display = display
        self.use_ai = use_ai

        self.reset()

    def reset(self):
        obs = None
        self.evManager = Event.EventManager()

        if self.name == 'Taxi Agent Editor':
            self.player = Player.Player(self.use_ai, self.evManager)

            if not self.use_ai:
                self.inputController = Player.InputController(self.evManager)

            self.character = Car.Car(Settings.CAR_IMAGE, self.evManager)
            self.map = Map.Map(self.evManager)
            self.mode = Game.Mode(Game.Mode.POINT_EDITING)

            self.game = Game.Game(self.player, self.character, self.map, self.mode, self.evManager)
            self.gameController = Game.GameController(self.evManager)

            if self.display:
                self.gameView = Game.GameView(self.game, self.evManager)

            self.evManager.post(Event.ChangeModeEvent(self.mode))

        return obs

    def run(self):
        self.gameController.run()

    def step(self):
        self.gameController.step()
