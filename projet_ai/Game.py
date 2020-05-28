from projet_ai import Event, Settings, Tools
import pygame
import math
from pygame import Vector2
import numpy as np


class GameView(Event.Listener):

	def __init__(self, game, evManager):
		super().__init__(evManager)

		# Create the screen
		self.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
		# self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # TODO: For the final version

		# Title and Icon
		pygame.display.set_caption("Taxi Agent")
		icon = pygame.image.load("taxi.png")
		pygame.display.set_icon(icon)

		self.game = game
		self.character = None

	def notify(self, event):
		if isinstance(event, Event.CarUpdatedEvent):
			self.character = event.car

	def render(self):
		self.draw_background()

		if self.game.mode == Mode.PLAY_MODE:
			self.play_mode()
		elif self.game.mode == Mode.POINT_EDITING:
			self.point_editing()
		elif self.game.mode == Mode.LINE_EDITING:
			self.line_editing()

		# Always update the display at the end of the loop
		pygame.display.update()

	def draw_background(self):
		self.screen.fill(Settings.GRASS_COLOR)

	def point_editing(self):
		for position in self.game.map.points:
			radius = Settings.MIN_DIST_POINTS
			transparent_circle = pygame.Surface((Settings.WIDTH, Settings.HEIGHT), pygame.SRCALPHA)
			pygame.draw.circle(transparent_circle, (150, 150, 150, 50), (radius * 2, radius * 2), radius - 2)
			pygame.draw.circle(transparent_circle, (200, 200, 200, 50), (radius * 2, radius * 2), radius, 2)
			self.screen.blit(transparent_circle, (position[0] - radius * 2, position[1] - radius * 2))
			pygame.draw.circle(self.screen, (100, 150, 255), position, 10)

		mouse = pygame.mouse.get_pos()
		if self.game.map.is_space_available(mouse):
			pygame.draw.circle(self.screen, (150, 150, 150), mouse, 8)
			pygame.draw.circle(self.screen, (200, 200, 200), mouse, 10, 2)
		else:
			pygame.draw.circle(self.screen, (150, 100, 100), mouse, 8)
			pygame.draw.circle(self.screen, (200, 150, 150), mouse, 10, 2)

	def line_editing(self):
		for position in self.game.map.points:
			radius = int(Settings.ROAD_WIDTH / 2)
			transparent_circle = pygame.Surface((Settings.WIDTH, Settings.HEIGHT), pygame.SRCALPHA)
			pygame.draw.circle(transparent_circle, (150, 150, 150, 50), (radius, radius), radius - 2)
			pygame.draw.circle(transparent_circle, (200, 200, 200, 50), (radius, radius), radius, 2)
			self.screen.blit(transparent_circle, (position[0] - radius, position[1] - radius))
			pygame.draw.circle(self.screen, Settings.ROAD_COLOR, position, 10)

		for line in self.game.map.lines:
			self.draw_rect(line, Settings.ROAD_COLOR, 20)

		line_to_mouse = self.game.map.get_building_line()
		if line_to_mouse is not None:
			if self.game.map.is_crossing(line_to_mouse):
				self.draw_rect(line_to_mouse, Settings.CROSSING_ROAD_COLOR, 20)
			else:
				self.draw_rect(line_to_mouse, Settings.ROAD_COLOR, 20)

	def draw_rect(self, line, color, width):
		rect = self.game.map.get_rect(line, width)
		if rect is not None:
			pygame.draw.polygon(self.screen, color, rect)

	def play_mode(self):
		# Draw the roads
		for position in self.game.map.points:
			pygame.draw.circle(self.screen, Settings.ROAD_COLOR, position, int(Settings.ROAD_WIDTH / 2))

		for line in self.game.map.lines:
			self.draw_rect(line, Settings.ROAD_COLOR, Settings.ROAD_WIDTH)

		# Draw the taxi
		if self.character is not None:
			self.draw_car()

			if Settings.DEBUG:
				self.draw_lidar()
				self.draw_lidar_points()
			self.draw_view((10, 10))

	def draw_car(self):
		car = self.character

		rotated = pygame.transform.rotate(car.image, car.angle)
		rect = rotated.get_rect(center=car.position)

		if Settings.DEBUG:
			pygame.draw.lines(self.screen, Settings.CAR_HITBOX_COLOR, True, car.get_hitbox())

		self.screen.blit(rotated, rect)

	def draw_view(self, pos):
		lidar = self.character.lidar

		x, y = pos
		border_size = Settings.LIDAR_VIEW_BORDER_SIZE
		square_size = Settings.LIDAR_VIEW_SQUARE_SIZE

		border = pygame.rect.Rect(x, y,
								  lidar.col * square_size + border_size * 2,
								  lidar.row * square_size + border_size * 2)
		pygame.draw.rect(self.screen, Settings.LIDAR_VIEW_BORDER_COLOR, border)
		x += border_size
		y += border_size
		for i in range(lidar.row):
			for j in range(lidar.col):
				square = pygame.rect.Rect(j * square_size + x, i * square_size + y, square_size, square_size)

				if lidar.matrix[i][j] == 0:
					pygame.draw.rect(self.screen, Settings.LIDAR_VIEW_GRASS, square)
				else:
					pygame.draw.rect(self.screen, Settings.LIDAR_VIEW_ROAD, square)

	def draw_lidar(self):
		pos = self.character.position
		angle = -math.radians(self.character.angle)
		lidar = self.character.lidar

		front = Tools.get_point_at_vector(pos, lidar.length - lidar.back_length, angle)
		front_right = Tools.get_point_at_vector(front, lidar.width / 2, math.pi / 2 + angle)
		front_left = Tools.get_point_at_vector(front, lidar.width / 2, angle - math.pi / 2)

		back = Tools.get_point_at_vector(pos, lidar.back_length, math.pi + angle)
		back_right = Tools.get_point_at_vector(back, lidar.width / 2, math.pi / 2 + angle)
		back_left = Tools.get_point_at_vector(back, lidar.width / 2, angle - math.pi / 2)

		lidar_corners = [front_left, back_left, back_right, front_right]
		pygame.draw.lines(self.screen, Settings.LIDAR_BOX_COLOR, True, lidar_corners)

	def draw_lidar_points(self):
		lidar = self.character.lidar
		pos = self.character.position
		angle = -self.character.angle

		vec = Vector2()
		vec.from_polar((lidar.length - lidar.back_length, angle))
		front = pos + vec

		vec.from_polar((lidar.width / 2, angle - 90))
		front_left = front + vec

		current = front_left

		for i in range(len(lidar.matrix)):
			first_of_line = Vector2(current)

			for j in range(len(lidar.matrix[i])):
				pygame.draw.circle(self.screen, Settings.LIDAR_POINTS_COLOR, (int(current.x), int(current.y)), 3)

				vec.from_polar((lidar.width / (lidar.col - 1), angle + 90))
				current += vec

			vec.from_polar((lidar.length / (lidar.row - 1), angle + 180))
			current = first_of_line + vec


class GameController(Event.Listener):

	def __init__(self, game, evManager):
		super().__init__(evManager)

		self.game = game
		self.keepGoing = True
		self.previous = 0
		self.step_counter = 0
		self.life_span = 500  # -1 = no life span
		self.step_grass_counter = 0
		self.life_span_on_grass = 20
		self.info = ''

	def run(self):

		while self.keepGoing:
			now = pygame.time.get_ticks()
			delta = (now - self.previous) / 1000.0
			self.previous = now

			self.evManager.post(Event.TickEvent(delta))

		pygame.quit()

	def step(self, action):
		self.evManager.post(Event.MovePlayerEvent(Vector2(action[0], action[1])))

		now = pygame.time.get_ticks()
		delta = (now - self.previous) / 1000.0
		self.previous = now

		self.evManager.post(Event.TickEvent(delta))

		car = self.game.character

		new_state = car.get_state()
		reward = abs(car.velocity[0]) / car.max_front_velocity if car.is_on_road() else -1
		done = not self.keepGoing

		self.step_counter += 1
		if self.step_counter == self.life_span:
			self.keepGoing = False

		if not car.is_on_road():
			self.step_grass_counter += 1
			if self.step_grass_counter == self.life_span_on_grass:
				self.keepGoing = False

		return new_state, reward, done, self.info

	def notify(self, event):
		if isinstance(event, Event.QuitEvent):
			self.info = 'Quit'
			self.keepGoing = False

		elif isinstance(event, Event.ToggleDebugEvent):
			Settings.DEBUG = not Settings.DEBUG

	def reset(self):
		self.keepGoing = True
		self.step_counter = 0
		self.step_grass_counter = 0


class Mode:
	PLAY_MODE = 0
	POINT_EDITING = 1
	LINE_EDITING = 2

	def __init__(self, mode):
		self.mode = mode

	def __eq__(self, other_mode):
		return self.mode == other_mode

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

	def __init__(self, player, character, map_, mode, evManager):
		super().__init__(evManager)

		self.player = player
		self.character = character
		self.map = map_
		self.mode = mode

		print('Press P to edit points, L to edit lines, F when you\'ve finished, D for debug and ESC to quit')

	def start(self):
		first_point = Vector2(self.map.get_point(0))
		next_point = Vector2(self.map.get_neighbours(0)[0])
		angle = math.degrees(math.atan2(first_point.y - next_point.y, first_point.x - next_point.x))
		if angle < 0:
			angle += 360
		self.character.reset(first_point, 180 - angle)

	def notify(self, event):
		if isinstance(event, Event.LoadMapEvent):
			self.map.load_map(event.map_name)
			if self.mode == Mode.PLAY_MODE:
				self.map.build()
				self.start()

		elif isinstance(event, Event.ChangeModeEvent):
			self.mode = event.mode
			if self.mode == Mode.PLAY_MODE:
				self.map.build()
				self.start()

		elif isinstance(event, Event.CreationEvent):
			# Point creation
			if self.mode == Mode.POINT_EDITING:
				self.map.create_point()

			# Line creation
			elif self.mode == Mode.LINE_EDITING:
				self.map.create_line()

		elif isinstance(event, Event.RemovingEvent):
			# Point removing
			if self.mode == Mode.POINT_EDITING:
				self.map.remove_point()

			# Cancel the new line drawing
			elif self.mode == Mode.LINE_EDITING:
				self.map.cancel_line()
