from projet_ai import Event, Settings, Game
import pygame
from pygame import Vector2


class InputController(Event.Listener):

	FRONT = 0
	BACK = 1
	LEFT = 2
	RIGHT = 3

	def __init__(self, evManager):
		super().__init__(evManager)

		self.key_maintained = [False for i in range(4)]

	def notify(self, event):
		if isinstance(event, Event.TickEvent):
			direction = Vector2(0, 0)

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

					elif event.key == Settings.KEY_MOVE_FRONT:
						self.key_maintained[InputController.FRONT] = True

					elif event.key == Settings.KEY_MOVE_BACK:
						self.key_maintained[InputController.BACK] = True

					elif event.key == Settings.KEY_MOVE_LEFT:
						self.key_maintained[InputController.LEFT] = True

					elif event.key == Settings.KEY_MOVE_RIGHT:
						self.key_maintained[InputController.RIGHT] = True

				elif event.type == pygame.KEYUP:
					if event.key == Settings.KEY_MOVE_FRONT:
						self.key_maintained[InputController.FRONT] = False

					elif event.key == Settings.KEY_MOVE_BACK:
						self.key_maintained[InputController.BACK] = False

					elif event.key == Settings.KEY_MOVE_LEFT:
						self.key_maintained[InputController.LEFT] = False

					elif event.key == Settings.KEY_MOVE_RIGHT:
						self.key_maintained[InputController.RIGHT] = False

				# If mouse is pressed
				elif event.type == pygame.MOUSEBUTTONDOWN:

					if event.button == Settings.MOUSE_CREATE:
						ev = Event.CreationEvent()

					elif event.button == Settings.MOUSE_REMOVE:
						ev = Event.RemovingEvent()

				if ev is not None:
					self.evManager.post(ev)

			if self.key_maintained[InputController.FRONT]:
				direction += Vector2(1, 0)

			if self.key_maintained[InputController.BACK]:
				direction += Vector2(-1, 0)

			if self.key_maintained[InputController.LEFT]:
				direction += Vector2(0, -1)

			if self.key_maintained[InputController.RIGHT]:
				direction += Vector2(0, 1)

			self.evManager.post(Event.MovePlayerEvent(direction))


class Player(Event.Listener):

	def __init__(self, use_ai, evManager):
		super().__init__(evManager)
		self.use_ai = use_ai
