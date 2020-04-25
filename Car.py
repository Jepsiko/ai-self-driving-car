import pygame
from pygame.math import Vector2


class Car:

	def __init__(self, img, x, y, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
		self.image = pygame.image.load(img)

		self.position = Vector2(x, y)

	def draw(self, screen):
		rect = self.image.get_rect()
		screen.blit(self.image, self.position - (rect.width / 2, rect.height / 2))

	def is_on_grass(self, screen):
		rect = self.image.get_rect()

		topleft = (int(self.position.x + rect.topleft[0]), int(self.position.y + rect.topleft[1]))
		bottomleft = (int(self.position.x + rect.bottomleft[0]), int(self.position.y + rect.bottomleft[1]))
		topright = (int(self.position.x + rect.topright[0]), int(self.position.y + rect.topright[1]))
		bottomright = (int(self.position.x + rect.bottomright[0]), int(self.position.y + rect.bottomright[1]))
		if screen.get_at(topleft) == (0, 50, 0, 255):
			return True
		elif screen.get_at(bottomleft) == (0, 50, 0, 255):
			return True
		elif screen.get_at(topright) == (0, 50, 0, 255):
			return True
		elif screen.get_at(bottomright) == (0, 50, 0, 255):
			return True
		else:
			return False
