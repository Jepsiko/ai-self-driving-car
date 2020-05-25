from projet_ai import Event, Settings, Tools
import pygame
import math
from pygame import Vector2


class GameView(Event.Listener):

	def __init__(self, game, evManager):
		super().__init__(evManager)

		pygame.init()

		# Create the screen
		self.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
		# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #  TODO: For the final version

		# Title and Icon
		pygame.display.set_caption("Taxi Agent")
		icon = pygame.image.load("taxi.png")
		pygame.display.set_icon(icon)

		self.game = game
		self.character = None

	def notify(self, event):
		if isinstance(event, Event.TickEvent):
			self.draw_background()

			if self.game.mode == Mode.PLAY_MODE:
				self.play_mode()
			elif self.game.mode == Mode.POINT_EDITING:
				self.point_editing()
			elif self.game.mode == Mode.LINE_EDITING:
				self.line_editing()

			# Always update the display at the end of the loop
			pygame.display.update()

		elif isinstance(event, Event.CarUpdatedEvent):
			self.character = event.car

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
			self.draw_line(line, Settings.ROAD_COLOR, 20)

		line_to_mouse = self.game.map.get_building_line()
		if line_to_mouse is not None:
			if self.game.map.is_crossing(line_to_mouse):
				self.draw_line(line_to_mouse, Settings.CROSSING_ROAD_COLOR, 20)
			else:
				self.draw_line(line_to_mouse, Settings.ROAD_COLOR, 20)

	def draw_line(self, line, color, width):
		pos1, pos2 = line
		x1, y1 = pos1
		x2, y2 = pos2
		length = math.hypot(x1 - x2, y1 - y2)
		if length == 0:
			return
		angle = math.acos((x2 - x1) / length)
		if y2 < y1:
			angle = math.pi * 2 - angle
		point1 = (x1 + int(width / 2 * math.cos(angle + math.pi / 2)),
				  y1 + int(width / 2 * math.sin(angle + math.pi / 2)))
		point2 = (x1 + int(width / 2 * math.cos(angle - math.pi / 2)),
				  y1 + int(width / 2 * math.sin(angle - math.pi / 2)))
		point3 = (x2 + int(width / 2 * math.cos(angle - math.pi / 2)),
				  y2 + int(width / 2 * math.sin(angle - math.pi / 2)))
		point4 = (x2 + int(width / 2 * math.cos(angle + math.pi / 2)),
				  y2 + int(width / 2 * math.sin(angle + math.pi / 2)))
		pygame.draw.polygon(self.screen, color, [point1, point2, point3, point4])

	def play_mode(self):
		# Draw the roads
		for position in self.game.map.points:
			pygame.draw.circle(self.screen, Settings.ROAD_COLOR, position, int(Settings.ROAD_WIDTH / 2))

		for line in self.game.map.lines:
			self.draw_line(line, Settings.ROAD_COLOR, Settings.ROAD_WIDTH)

		# Draw the taxi
		if self.character is not None:
			self.draw_car()

			if Settings.DEBUG:
				self.draw_lidar()
				self.draw_lidar_points()
			self.draw_view((10, 10))

	def update(self):
		car = self.taxi
		delta = pygame.time.Clock().get_time() / 1000

		keys = pygame.key.get_pressed()

		x = 0
		y = 0

		# Key board pressed
		if keys[pygame.K_UP]:
			# print("up")
			car.position.y -= 1
			y -= 1

		if keys[pygame.K_DOWN]:
			# print("down")
			car.position.y += 1
			y += 1

		if keys[pygame.K_LEFT]:
			# print("gauche")
			car.position.x -= 1
			x -= 1

		if keys[pygame.K_RIGHT]:
			# print("droite")
			car.position.x += 1
			x += 1

		if x == 0 and y == 0:
			car.direction = Vector2(x, y)

		else:
			car.direction = Vector2(x, y).normalize()

		car.update(delta)
		car.lidar.update(self.screen, car.position, -math.radians(car.angle))

	def draw_car(self):
		car = self.character

		rotated = pygame.transform.rotate(car.image, car.angle)
		rect = rotated.get_rect(center=car.position)

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
		pos = self.character.position
		angle = -math.radians(self.character.angle)
		lidar = self.character.lidar

		front = Tools.get_point_at_vector(pos, lidar.length - lidar.back_length, angle)
		front_left = Tools.get_point_at_vector(front, lidar.width / 2, angle - math.pi / 2)

		current = front_left

		for i in range(len(lidar.matrix)):
			first_of_line = current
			for j in range(len(lidar.matrix[i])):
				pygame.draw.circle(self.screen, Settings.LIDAR_POINTS_COLOR, (int(current.x), int(current.y)), 3)

				current = Tools.get_point_at_vector(current, lidar.width / (lidar.col - 1), math.pi / 2 + angle)
			current = Tools.get_point_at_vector(first_of_line, lidar.length / (lidar.row - 1), math.pi + angle)

	def is_on_grass(self):
		angle = -math.radians(self.character.angle)
		car = self.character

		front = Tools.get_point_at_vector(car.position, car.length / 2, angle)
		front_right = Tools.get_point_at_vector(front, car.width / 2, math.pi / 2 + angle)
		front_left = Tools.get_point_at_vector(front, car.width / 2, angle - math.pi / 2)

		back = Tools.get_point_at_vector(car.position, car.length / 2, math.pi + angle)
		back_right = Tools.get_point_at_vector(back, car.width / 2, math.pi / 2 + angle)
		back_left = Tools.get_point_at_vector(back, car.width / 2, angle - math.pi / 2)

		on_grass = False
		if self.screen.get_at((int(front_left.x), int(front_left.y))) == Settings.GRASS_COLOR:
			on_grass = True
		elif self.screen.get_at((int(front_right.x), int(front_right.y))) == Settings.GRASS_COLOR:
			on_grass = True
		elif self.screen.get_at((int(back_left.x), int(back_left.y))) == Settings.GRASS_COLOR:
			on_grass = True
		elif self.screen.get_at((int(back_right.x), int(back_right.y))) == Settings.GRASS_COLOR:
			on_grass = True

		# Draw the hitbox of the car
		if Settings.DEBUG:
			lidar_corners = [front_left, back_left, back_right, front_right]
			pygame.draw.lines(self.screen, Settings.CAR_HITBOX_COLOR, True, lidar_corners)

		return on_grass

	def change_car_position(self, position):
		self.character.position = position


class GameController(Event.Listener):

	def __init__(self, evManager):
		super().__init__(evManager)

		self.keepGoing = 1

	def run(self):
		clock = pygame.time.Clock()
		while self.keepGoing:

			self.evManager.post(Event.TickEvent())

			clock.tick(10)

		pygame.quit()

	def step(self):
		pass

	def notify(self, event):
		if isinstance(event, Event.QuitEvent):
			self.keepGoing = 0

		elif isinstance(event, Event.ToggleDebugEvent):
			Settings.DEBUG = not Settings.DEBUG


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

	def notify(self, event):
		if isinstance(event, Event.ChangeModeEvent):
			self.mode = event.mode
			if self.mode == Mode.PLAY_MODE:
				self.map.build()
				self.character.set_position(self.map.get_point(0))

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
