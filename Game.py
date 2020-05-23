import pygame
import Event
import Map
import Player


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
				if event.type == pygame.KEYDOWN:

					# "ESC" to Quit
					if event.key == pygame.K_ESCAPE:
						ev = Event.QuitEvent()

					# "P" to enter Point editing mode
					if event.key == pygame.K_p:
						ev = Event.ChangeModeEvent(Mode(Mode.POINT_EDITING))

					# "L" to enter Line editing mode
					if event.key == pygame.K_l:
						ev = Event.ChangeModeEvent(Mode(Mode.LINE_EDITING))

					# "F" to Finish editing
					if event.key == pygame.K_f:
						ev = Event.ChangeModeEvent(Mode(Mode.PLAY_MODE))

					# "D" to enter Debug mode
					if event.key == pygame.K_d:
						ev = Event.ToggleDebugEvent()

				# If mouse is pressed
				if event.type == pygame.MOUSEBUTTONDOWN:

					# Left clic pressed
					if event.button == 1:
						ev = Event.LeftClicPressedEvent()

					# Right clic pressed
					if event.button == 3:
						ev = Event.RightClicPressedEvent()

				if ev is not None:
					self.post(ev)


class GameController(Event.Listener):

	def __init__(self, evManager):
		super().__init__(evManager)

		self.keepGoing = 1

	def run(self):
		# clock = pygame.time.Clock()
		# elapsed_frames = 0

		while self.keepGoing:
			# delay = clock.tick(10)
			# if elapsed_frames % 100 == 1:
			# 	pass

			self.post(Event.TickEvent())
			# elapsed_frames += 1

		pygame.quit()

	def notify(self, event):
		if isinstance(event, Event.QuitEvent):
			self.keepGoing = 0


class Mode:
	PLAY_MODE = 0
	POINT_EDITING = 1
	LINE_EDITING = 2

	def __init__(self, mode):
		self.mode = mode

	def __eq__(self, other):
		return self.mode == other

	def __str__(self):
		if self.mode == Mode.PLAY_MODE:
			return 'Play Mode'
		elif self.mode == Mode.POINT_EDITING:
			return 'Point Editing Mode'
		elif self.mode == Mode.LINE_EDITING:
			return 'Line Editing Mode'
		else:
			return 'Mode Error'


class Game(Event.Listener):

	def __init__(self, evManager):
		super().__init__(evManager)

		self.player = Player.Player(evManager)
		self.map = Map.Map(evManager)
		self.mode = Mode(Mode.POINT_EDITING)
		self.post(Event.ChangeModeEvent(self.mode))

		print("Press P to edit points, L to edit lines, F when you've finished, D for debug and ESC to quit")

	def start(self):
		pass

	def notify(self, event):
		if isinstance(event, Event.TickEvent):
			pass

		elif isinstance(event, Event.ChangeModeEvent):
			self.mode = event.mode
			if self.mode == Mode.PLAY_MODE:
				self.map.build()

		elif isinstance(event, Event.LeftClicPressedEvent):
			# Point creation
			if self.mode == Mode.POINT_EDITING:
				self.map.create_point()

			# Line creation
			if self.mode == Mode.LINE_EDITING:
				self.map.create_line()

		elif isinstance(event, Event.RightClicPressedEvent):
			# Point removing
			if self.mode == Mode.POINT_EDITING:
				self.map.remove_point()

			# Cancel the new line drawing
			if self.mode == Mode.LINE_EDITING:
				self.map.cancel_line()
