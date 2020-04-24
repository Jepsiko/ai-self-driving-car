import pygame
from pygame.math import Vector2
from math import sin, radians, degrees


class Car:

	def __init__(self, img, x, y, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
		self.image = pygame.image.load(img)

		self.position = Vector2(x, y)

	def draw(self, screen):
		rect = self.image.get_rect()
		screen.blit(self.image, self.position - (rect.width / 2, rect.height / 2))
