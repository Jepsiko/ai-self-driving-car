import pygame
import settings
from tools import *
from Car import Car


class GameUI:

	def __init__(self):
		# Create the screen
		self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
		# screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN) #  For the final version

		# Title and Icon
		pygame.display.set_caption("Taxi Agent")
		icon = pygame.image.load("taxi.png")
		pygame.display.set_icon(icon)

		# Taxi taxi
		self.taxi = Car("car.png", 0, 0)

	def draw_background(self):
		self.screen.fill(settings.GRASS_COLOR)

	def point_editing(self, points):
		mouseX, mouseY = pygame.mouse.get_pos()

		spaceAvailable = True
		for position in points:
			radius = settings.MIN_DIST_POINTS
			transparent_circle = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
			pygame.draw.circle(transparent_circle, (150, 150, 150, 50), (radius * 2, radius * 2), radius - 2)
			pygame.draw.circle(transparent_circle, (200, 200, 200, 50), (radius * 2, radius * 2), radius, 2)
			self.screen.blit(transparent_circle, (position[0] - radius * 2, position[1] - radius * 2))
			pygame.draw.circle(self.screen, (100, 150, 255), position, 10)

			if math.hypot(position[0] - mouseX, position[1] - mouseY) <= settings.MIN_DIST_POINTS:
				spaceAvailable = False

		# If the mouse is in the window
		if pygame.mouse.get_focused():
			if spaceAvailable:
				pygame.draw.circle(self.screen, (150, 150, 150), (mouseX, mouseY), 8)
				pygame.draw.circle(self.screen, (200, 200, 200), (mouseX, mouseY), 10, 2)
			else:
				pygame.draw.circle(self.screen, (150, 100, 100), (mouseX, mouseY), 8)
				pygame.draw.circle(self.screen, (200, 150, 150), (mouseX, mouseY), 10, 2)

			# Add a new point
			if pygame.mouse.get_pressed()[0] and spaceAvailable:
				points.append((mouseX, mouseY))

	def line_editing(self, points, lines, startingPoint, endingPoint):
		mouseX, mouseY = pygame.mouse.get_pos()

		for position in points:
			radius = int(settings.ROAD_WIDTH / 2)
			transparent_circle = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
			pygame.draw.circle(transparent_circle, (150, 150, 150, 50), (radius, radius), radius - 2)
			pygame.draw.circle(transparent_circle, (200, 200, 200, 50), (radius, radius), radius, 2)
			self.screen.blit(transparent_circle, (position[0] - radius, position[1] - radius))
			pygame.draw.circle(self.screen, settings.ROAD_COLOR, position, 10)

		crossing = False
		for line in lines:
			self.draw_line(line, settings.ROAD_COLOR, 20)

			if startingPoint is not None and is_line_crossing(line, (startingPoint, (mouseX, mouseY))):
				crossing = True

		if startingPoint is not None:
			line_to_mouse = (startingPoint, (mouseX, mouseY))
			if crossing:
				self.draw_line(line_to_mouse, settings.CROSSING_ROAD_COLOR, 20)
			else:
				self.draw_line(line_to_mouse, settings.ROAD_COLOR, 20)

		# Add a new line
		if endingPoint is not None:
			lines.append([startingPoint, endingPoint])

			startingPoint = None
			endingPoint = None

		return startingPoint, endingPoint

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

	def game(self, points, lines):
		# Draw the roads
		radius = int(settings.ROAD_WIDTH / 2)
		for position in points:
			pygame.draw.circle(self.screen, settings.ROAD_COLOR, position, radius)

		for line in lines:
			self.draw_line(line, settings.ROAD_COLOR, settings.ROAD_WIDTH)

		# Update the game
		self.update()

		# Draw the taxi
		self.draw_car()
		if settings.DEBUG:
			self.draw_lidar()
			self.draw_lidar_points()
		self.draw_view((10, 10))
		if self.is_on_grass():
			print("WOW !!")

	def update(self):
		self.taxi.update(self.screen)

	def draw_car(self):
		car = self.taxi

		rotated = pygame.transform.rotate(car.image, car.angle)
		rect = rotated.get_rect(center=car.position)

		self.screen.blit(rotated, rect)

	def draw_view(self, pos):
		lidar = self.taxi.lidar

		x, y = pos
		border_size = settings.LIDAR_VIEW_BORDER_SIZE
		square_size = settings.LIDAR_VIEW_SQUARE_SIZE

		border = pygame.rect.Rect(x, y,
								  lidar.col * square_size + border_size * 2,
								  lidar.row * square_size + border_size * 2)
		pygame.draw.rect(self.screen, settings.LIDAR_VIEW_BORDER_COLOR, border)
		x += border_size
		y += border_size
		for i in range(lidar.row):
			for j in range(lidar.col):
				square = pygame.rect.Rect(j * square_size + x, i * square_size + y, square_size, square_size)

				if lidar.matrix[i][j] == 0:
					pygame.draw.rect(self.screen, settings.LIDAR_VIEW_GRASS, square)
				else:
					pygame.draw.rect(self.screen, settings.LIDAR_VIEW_ROAD, square)

	def draw_lidar(self):
		pos = self.taxi.position
		angle = -math.radians(self.taxi.angle)
		lidar = self.taxi.lidar

		front = get_point_at_vector(pos, lidar.length - lidar.back_length, angle)
		front_right = get_point_at_vector(front, lidar.width / 2, math.pi / 2 + angle)
		front_left = get_point_at_vector(front, lidar.width / 2, angle - math.pi / 2)

		back = get_point_at_vector(pos, lidar.back_length, math.pi + angle)
		back_right = get_point_at_vector(back, lidar.width / 2, math.pi / 2 + angle)
		back_left = get_point_at_vector(back, lidar.width / 2, angle - math.pi / 2)

		lidar_corners = [front_left, back_left, back_right, front_right]
		pygame.draw.lines(self.screen, settings.LIDAR_BOX_COLOR, True, lidar_corners)

	def draw_lidar_points(self):
		pos = self.taxi.position
		angle = -math.radians(self.taxi.angle)
		lidar = self.taxi.lidar

		front = get_point_at_vector(pos, lidar.length - lidar.back_length, angle)
		front_left = get_point_at_vector(front, lidar.width / 2, angle - math.pi / 2)

		current = front_left

		for i in range(len(lidar.matrix)):
			first_of_line = current
			for j in range(len(lidar.matrix[i])):
				pygame.draw.circle(self.screen, settings.LIDAR_POINTS_COLOR, (int(current.x), int(current.y)), 3)

				current = get_point_at_vector(current, lidar.width / (lidar.col - 1), math.pi / 2 + angle)
			current = get_point_at_vector(first_of_line, lidar.length / (lidar.row - 1), math.pi + angle)

	def is_on_grass(self):
		angle = -math.radians(self.taxi.angle)
		car = self.taxi

		front = get_point_at_vector(car.position, car.length / 2, angle)
		front_right = get_point_at_vector(front, car.width / 2, math.pi / 2 + angle)
		front_left = get_point_at_vector(front, car.width / 2, angle - math.pi / 2)

		back = get_point_at_vector(car.position, car.length / 2, math.pi + angle)
		back_right = get_point_at_vector(back, car.width / 2, math.pi / 2 + angle)
		back_left = get_point_at_vector(back, car.width / 2, angle - math.pi / 2)

		on_grass = False
		if self.screen.get_at((int(front_left.x), int(front_left.y))) == settings.GRASS_COLOR:
			on_grass = True
		elif self.screen.get_at((int(front_right.x), int(front_right.y))) == settings.GRASS_COLOR:
			on_grass = True
		elif self.screen.get_at((int(back_left.x), int(back_left.y))) == settings.GRASS_COLOR:
			on_grass = True
		elif self.screen.get_at((int(back_right.x), int(back_right.y))) == settings.GRASS_COLOR:
			on_grass = True

		# Draw the hitbox of the car
		if settings.DEBUG:
			lidar_corners = [front_left, back_left, back_right, front_right]
			pygame.draw.lines(self.screen, settings.CAR_HITBOX_COLOR, True, lidar_corners)

		return on_grass

	def change_car_position(self, position):
		self.taxi.position = position
