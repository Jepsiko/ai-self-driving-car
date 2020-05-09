import pygame
from pygame.math import Vector2
from Sensor import Sensor


class Car:

	def __init__(self, img, x, y):
		self.image = pygame.image.load(img)

		self.position = Vector2(x, y)
		print("pos", self.position)

	def draw(self, screen):
		rect = self.image.get_rect()
		screen.blit(self.image, self.position - (rect.width / 2, rect.height / 2))
		self.create_sensor(4)

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

	def get_pos(self):
		return self.position

	def create_sensor(self, nbr_sensor):
		sensors = []
		length = 200
		x = 0
		while x != nbr_sensor:
			sensor = Sensor(self.position, length)
			sensors.append(sensor)
			x += 1
		print(sensors)