import pygame
from pygame.math import Vector2


class Car:

	def __init__(self, img, x, y, heading=0.0):
		self.image = pygame.image.load(img)

		self.position = Vector2(x, y)
		self.heading = heading
		self.velocity = Vector2()
		self.accel = Vector2()
		self.steerAngle = 0.0

	def draw(self, screen):
		rect = self.image.get_rect()
		screen.blit(self.image, self.position - (rect.width / 2, rect.height / 2))

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
