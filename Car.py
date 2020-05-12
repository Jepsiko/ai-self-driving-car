import pygame
from pygame.math import Vector2
from Lidar import Lidar
import math


class Car:

	def __init__(self, img, x, y):
		self.image = pygame.image.load(img)

		self.position = Vector2(x, y)
		self.lidar = Lidar(7, 6)
		self.rotation = 0

	def draw(self, screen):
		rot = self.rotation
		rotated = pygame.transform.rotate(self.image, rot)

		rect = rotated.get_rect(center=self.position)

		screen.blit(rotated, rect)

	def draw_lidar(self, screen):
		self.lidar.draw(screen, self.position, -math.radians(self.rotation))

	def draw_view(self, screen, pos):
		self.lidar.draw_view(screen, pos)

	def is_on_grass(self, screen, grassColor):
		rect = self.image.get_rect()
		topleft = (int(self.position.x + rect.topleft[0]), int(self.position.y + rect.topleft[1]))
		bottomleft = (int(self.position.x + rect.bottomleft[0]), int(self.position.y + rect.bottomleft[1]))
		topright = (int(self.position.x + rect.topright[0]), int(self.position.y + rect.topright[1]))
		bottomright = (int(self.position.x + rect.bottomright[0]), int(self.position.y + rect.bottomright[1]))

		if screen.get_at(topleft) == grassColor:
			return True
		elif screen.get_at(bottomleft) == grassColor:
			return True
		elif screen.get_at(topright) == grassColor:
			return True
		elif screen.get_at(bottomright) == grassColor:
			return True
		else:
			return False

	def update(self, screen):
		self.rotation += 0.1  # TEMP
		self.lidar.update(screen, self.position, -math.radians(self.rotation))
