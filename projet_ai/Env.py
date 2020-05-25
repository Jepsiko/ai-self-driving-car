from projet_ai import Event, Player, Car, Map, Settings, Game


class Env:
    def __init__(self, name='Taxi Agent'):
        self.name = name
        self.evManager = Event.EventManager()

        if self.name == 'Taxi Agent':
            self.player = Player.Player(self.evManager)
            self.inputController = Player.InputController(self.evManager)
            self.character = Car.Car(Settings.CAR_IMAGE, self.evManager)
            self.map = Map.Map(self.evManager)
            self.mode = Game.Mode(Game.Mode.POINT_EDITING)

            self.game = Game.Game(self.player, self.character, self.map, self.mode, self.evManager)
            self.gameController = Game.GameController(self.evManager)
            self.gameView = Game.GameView(self.game, self.evManager)

            self.evManager.post(Event.ChangeModeEvent(self.mode))

    def reset(self):
        obs = None
        self.evManager = Event.EventManager()

        if self.name == 'Taxi Agent':
            self.player = Player.Player(self.evManager)
            self.inputController = Player.InputController(self.evManager)
            self.character = Car.Car(Settings.CAR_IMAGE, self.evManager)
            self.map = Map.Map(self.evManager)
            self.mode = Game.Mode(Game.Mode.POINT_EDITING)

            self.game = Game.Game(self.player, self.character, self.map, self.mode, self.evManager)
            self.gameController = Game.GameController(self.evManager)
            self.gameView = Game.GameView(self.game, self.evManager)

            self.evManager.post(Event.ChangeModeEvent(self.mode))

        return obs

    def run(self):
        self.gameController.run()

    def step(self):
        pass
