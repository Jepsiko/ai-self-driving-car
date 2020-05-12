import pygame
import settings


class GameUI:

	def __init__(self):
		# Create the screen
		self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
		# screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN) #  For the final version

		# Title and Icon
		pygame.display.set_caption("Taxi Agent")
		icon = pygame.image.load("taxi.png")
		pygame.display.set_icon(icon)

	def draw_background(self):
		self.screen.fill(settings.GRASS_COLOR)
