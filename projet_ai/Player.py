from projet_ai import Event, Settings, Game
import pygame
from pygame import Vector2


class InputController(Event.Listener):

	def __init__(self, evManager):
		super().__init__(evManager)

		self.key_maintained = [False for i in range(4)]

	def notify(self, event):
		if isinstance(event, Event.TickEvent):
			for event in pygame.event.get():

				ev = None

				# Quit event from pygame
				if event.type == pygame.QUIT:
					ev = Event.QuitEvent()

				# If keyboard key is pressed
				elif event.type == pygame.KEYDOWN:

					if event.key == Settings.KEY_QUIT:
						ev = Event.QuitEvent()

					elif event.key == Settings.KEY_POINT_EDITING:
						ev = Event.ChangeModeEvent(Game.Mode(Game.Mode.POINT_EDITING))

					elif event.key == Settings.KEY_LINE_EDITING:
						ev = Event.ChangeModeEvent(Game.Mode(Game.Mode.LINE_EDITING))

					elif event.key == Settings.KEY_PLAY_MODE:
						ev = Event.ChangeModeEvent(Game.Mode(Game.Mode.PLAY_MODE))

					elif event.key == Settings.KEY_TOGGLE_DEBUG:
						ev = Event.ToggleDebugEvent()

					elif event.key == Settings.KEY_SAVE_MAP:
						ev = Event.SaveMapEvent(input('Map name : '))

					elif event.key == Settings.KEY_LOAD_MAP:
						ev = Event.LoadMapEvent(input('Map name : '))

				# If mouse is pressed
				elif event.type == pygame.MOUSEBUTTONDOWN:

					if event.button == Settings.MOUSE_CREATE:
						ev = Event.CreationEvent()

					elif event.button == Settings.MOUSE_REMOVE:
						ev = Event.RemovingEvent()

				if ev is not None:
					self.evManager.post(ev)

			# Keyboard inputs that has to be maintained
			key_pressed = pygame.key.get_pressed()
			direction = Vector2(0, 0)

			if key_pressed[Settings.KEY_MOVE_FRONT]:
				direction += Vector2(1, 0)

			if key_pressed[Settings.KEY_MOVE_BACK]:
				direction += Vector2(-1, 0)

			if key_pressed[Settings.KEY_MOVE_LEFT]:
				direction += Vector2(0, 1)

			if key_pressed[Settings.KEY_MOVE_RIGHT]:
				direction += Vector2(0, -1)

			if direction.x != 0 or direction.y != 0:
				self.evManager.post(Event.MovePlayerEvent(direction))


class Player(Event.Listener):

	def __init__(self, evManager):
		super().__init__(evManager)
		self.inputController = InputController(self.evManager)
