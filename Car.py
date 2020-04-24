import pygame


class Car:

	def __init__(self, img, x, y):
		self.carImg = pygame.image.load(img)
		self.carX = x
		self.carY = y

	def draw(self, screen):
		screen.blit(self.carImg, (self.carX, self.carY))
