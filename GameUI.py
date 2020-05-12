import pygame
import settings
from tools import *


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

	def draw_game(self, points, lines, taxi):
		# Draw the roads
		radius = int(settings.ROAD_WIDTH / 2)
		for position in points:
			pygame.draw.circle(self.screen, settings.ROAD_COLOR, position, radius)

		for line in lines:
			self.draw_line(line, settings.ROAD_COLOR, settings.ROAD_WIDTH)

		# # Draw the reward gates
		# colorRewardGates = (81, 81, 81)
		# global DEBUG
		# if DEBUG:
		# 	colorRewardGates = (255, 0, 0)
		# for road in rewardGates:
		# 	for line in road:
		# 		pygame.draw.line(screen, colorRewardGates, line[0], line[1], 2)

		# Draw the taxi
		taxi.update(self.screen)
		taxi.draw(self.screen)
		taxi.draw_view(self.screen, (10, 10))
		if taxi.is_on_grass(self.screen):
			pass
