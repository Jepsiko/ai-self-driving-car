from projet_ai import Event, Settings, Game
import pygame


class InputController(Event.Listener):

	def __init__(self, evManager):
		super().__init__(evManager)

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

				# If mouse is pressed
				elif event.type == pygame.MOUSEBUTTONDOWN:

					if event.button == Settings.MOUSE_CREATE:
						ev = Event.CreationEvent()

					elif event.button == Settings.MOUSE_REMOVE:
						ev = Event.RemovingEvent()

				if ev is not None:
					self.evManager.post(ev)


class Player(Event.Listener):

	def __init__(self, evManager):
		super().__init__(evManager)
