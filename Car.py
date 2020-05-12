import pygame
from Lidar import Lidar
import settings
from tools import *


class Car:

	def __init__(self, img, x, y):
		self.image = pygame.image.load(img)
		self.width = self.image.get_rect().height
		self.length = self.image.get_rect().width

		self.position = Vector2(x, y)
		self.lidar = Lidar(7, 6)
		self.angle = 0

	def draw(self, screen):
		rot = self.angle
		rotated = pygame.transform.rotate(self.image, rot)

		rect = rotated.get_rect(center=self.position)

		screen.blit(rotated, rect)

		if settings.DEBUG:
			self.lidar.draw(screen, self.position, -math.radians(self.angle))

	def draw_view(self, screen, pos):
		self.lidar.draw_view(screen, pos)

	def is_on_grass(self, screen):
		angle = -math.radians(self.angle)

		front = get_point_at_vector(self.position, self.length / 2, angle)
		front_right = get_point_at_vector(front, self.width / 2, math.pi / 2 + angle)
		front_left = get_point_at_vector(front, self.width / 2, angle - math.pi / 2)

		back = get_point_at_vector(self.position, self.length / 2, math.pi + angle)
		back_right = get_point_at_vector(back, self.width / 2, math.pi / 2 + angle)
		back_left = get_point_at_vector(back, self.width / 2, angle - math.pi / 2)

		on_grass = False
		if screen.get_at((int(front_left.x), int(front_left.y))) == settings.GRASS_COLOR:
			on_grass = True
		elif screen.get_at((int(front_right.x), int(front_right.y))) == settings.GRASS_COLOR:
			on_grass = True
		elif screen.get_at((int(back_left.x), int(back_left.y))) == settings.GRASS_COLOR:
			on_grass = True
		elif screen.get_at((int(back_right.x), int(back_right.y))) == settings.GRASS_COLOR:
			on_grass = True

		# Draw the hitbox of the car
		if settings.DEBUG:
			lidar_corners = [front_left, back_left, back_right, front_right]
			pygame.draw.lines(screen, settings.CAR_HITBOX_COLOR, True, lidar_corners)

		return on_grass

	def update(self, screen):
		self.angle += 0.1  # TEMP
		self.lidar.update(screen, self.position, -math.radians(self.angle))
