import pygame
from Lidar import Lidar
from tools import *


class Car:

	def __init__(self, img, x, y):
		self.image = pygame.image.load(img)
		self.width = self.image.get_rect().height
		self.length = self.image.get_rect().width

		self.position = Vector2(x, y)
		self.lidar = Lidar(7, 6)
		self.angle = 0

	def update(self, screen):
		self.angle += 0.1  # TEMP
		self.lidar.update(screen, self.position, -math.radians(self.angle))
