import pygame
from Graph import Graph
import settings
import tools
import math
from GameUI import GameUI
from pygame import Vector2
import Event


class Listener:

	def __init__(self, evManager):
		self.evManager = evManager
		if self.evManager is not None:
			self.evManager.register_listener(self)

	def post(self, event):
		self.evManager.post(event)

	def notify(self, event):
		pass


class Map(Listener):

	def __init__(self, evManager):
		super().__init__(evManager)

		self.firstPoint = None
		self.crossing = False

		self.points = []
		self.lines = []

		self.graph = None

	def build(self):
		self.graph = Graph(self.points, self.lines)
		return self.graph

	def get_graph(self):
		return self.graph

	def create_point(self):
		# Add a new point
		mouse = pygame.mouse.get_pos()
		if self.is_space_available(mouse):
			self.points.append(mouse)
			print("Point created !")

	def create_line(self):
		for point in self.points:
			mouse = pygame.mouse.get_pos()
			if Map.is_point_selected(point, mouse):

				# First point selected
				if self.firstPoint is None:
					self.firstPoint = point

				# Second point selected
				elif point != self.firstPoint and not self.is_crossing(mouse):

					# Creation of a new line
					print("Line created !")
					self.lines.append([self.firstPoint, point])
					self.firstPoint = None

	def remove_point(self):
		# Remove the point and all lines connected to it
		mouse = pygame.mouse.get_pos()
		point_to_remove = self.get_point_selected(mouse)

		if point_to_remove is not None:
			self.points.remove(point_to_remove)

			for line in reversed(self.lines):
				if point_to_remove in line:
					self.lines.remove(line)
					print("Point removed !")

	def cancel_line(self):
		self.firstPoint = None

	def is_crossing(self, mouse):
		for line in self.lines:
			if self.firstPoint is not None and tools.is_line_crossing(line, (self.firstPoint, mouse)):
				return True
		return False

	def is_space_available(self, mouse):
		# If the mouse is out of the screen
		if not pygame.mouse.get_focused():
			return False

		for point in self.points:
			if math.hypot(point[0] - mouse[0], point[1] - mouse[1]) <= settings.MIN_DIST_POINTS:
				return False
		return True

	def get_point_selected(self, mouse):
		for point in self.points:
			if Map.is_point_selected(point, mouse):
				return point
		return None

	@staticmethod
	def is_point_selected(point, mouse):
		return math.hypot(point[0] - mouse[0], point[1] - mouse[1]) <= settings.DIST_SELECT_POINT


class KeyboardController(Listener):

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


class GameController(Listener):

	def __init__(self, evManager):
		super().__init__(evManager)

		self.keepGoing = 1

	def run(self):
		clock = pygame.time.Clock()
		elapsed_frames = 0
		while self.keepGoing:
			delay = clock.tick(100)
			if elapsed_frames % 100 == 1:
				pass

			self.post(Event.TickEvent())
			elapsed_frames += 1

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


class Game(Listener):

	def __init__(self, evManager):
		super().__init__(evManager)

		self.map = Map(evManager)
		self.mode = Mode(Mode.POINT_EDITING)

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


class GameView(Listener):

	def __init__(self, evManager):
		super().__init__(evManager)

		pygame.init()
		self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))

	def notify(self, event):
		if isinstance(event, Event.TickEvent):
			pass
			# Always update the display at the end of the loop
			pygame.display.update()


def main():
	evManager = Event.EventManager()

	keybd = KeyboardController(evManager)
	game = Game(evManager)
	gameController = GameController(evManager)
	gameView = GameView(evManager)

	gameController.run()


if __name__ == "__main__":
	main()

