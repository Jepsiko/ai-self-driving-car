import pygame
import math
from Car import Car

WIDTH = 1366
HEIGHT = 768
MIN_DIST_POINTS = 150


if __name__ == "__main__":
	# Initialize pygame
	pygame.init()

	# Create the screen
	screen = pygame.display.set_mode((WIDTH, HEIGHT))

	# Title and Icon
	pygame.display.set_caption("Taxi Agent")
	icon = pygame.image.load("taxi.png")
	pygame.display.set_icon(icon)

	# Taxi taxi
	taxi = Car("car.png", 400, 300)

	# Level creation
	pointEditing = True
	lineEditing = False
	startingPoint = None
	endingPoint = None
	points = []
	lines = []

	# Game Loop
	running = True
	while running:

		# Event handling
		for event in pygame.event.get():

			# If the red cross in the upper right corner is clicked
			if event.type == pygame.QUIT:
				running = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if lineEditing:
						mouseX, mouseY = pygame.mouse.get_pos()
						for position in points:
							if math.hypot(position[0] - mouseX, position[1] - mouseY) <= 20:
								if startingPoint is None:
									startingPoint = position
								elif position != startingPoint:
									endingPoint = position

			# If keyboard key is pressed
			if event.type == pygame.KEYDOWN:

				# Point editing mode
				if event.key == pygame.K_p:
					pointEditing = True
					lineEditing = False

				# Line editing mode
				if event.key == pygame.K_l:
					lineEditing = True
					pointEditing = False

				# Line editing mode
				if event.key == pygame.K_f:
					lineEditing = False
					pointEditing = False

		# Change the background color
		screen.fill((0, 50, 0))

		# Level editing GUI
		mouseX, mouseY = pygame.mouse.get_pos()
		if pointEditing:
			if pygame.mouse.get_focused():

				spaceAvailable = True
				for position in points:

					pygame.draw.circle(screen, (100, 150, 255), position, 10)
					radius = MIN_DIST_POINTS
					transparent_circle = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
					pygame.draw.circle(transparent_circle, (150, 150, 150, 50), (radius*2, radius*2), radius-2)
					pygame.draw.circle(transparent_circle, (200, 200, 200, 50), (radius*2, radius*2), radius, 2)
					screen.blit(transparent_circle, (position[0] - radius*2, position[1] - radius*2))

					if math.hypot(position[0] - mouseX, position[1] - mouseY) <= MIN_DIST_POINTS:
						spaceAvailable = False

				if spaceAvailable:
					pygame.draw.circle(screen, (150, 150, 150), (mouseX, mouseY), 8)
					pygame.draw.circle(screen, (200, 200, 200), (mouseX, mouseY), 10, 2)
				else:
					pygame.draw.circle(screen, (150, 100, 100), (mouseX, mouseY), 8)
					pygame.draw.circle(screen, (200, 150, 150), (mouseX, mouseY), 10, 2)

				if pygame.mouse.get_pressed()[0] and spaceAvailable:
					points.append((mouseX, mouseY))

		elif lineEditing:
			for position in points:
				pygame.draw.circle(screen, (100, 150, 255), position, 10)
				radius = int(MIN_DIST_POINTS/4)
				transparent_circle = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
				pygame.draw.circle(transparent_circle, (150, 150, 150, 50), (radius, radius), radius-2)
				pygame.draw.circle(transparent_circle, (200, 200, 200, 50), (radius, radius), radius, 2)
				screen.blit(transparent_circle, (position[0] - radius, position[1] - radius))

			if startingPoint is not None:
				pygame.draw.line(screen, (100, 100, 100), startingPoint, (mouseX, mouseY), 20)

			if endingPoint is not None:

				lines.append([startingPoint, endingPoint])

				startingPoint = None
				endingPoint = None

			for line in lines:
				pygame.draw.line(screen, (100, 100, 100), line[0], line[1], 20)

		else:
			roadWidth = 70
			radius = int(roadWidth/2)
			for position in points:
				pygame.draw.circle(screen, (100, 100, 100), position, radius)

			for line in lines:
				pygame.draw.line(screen, (100, 100, 100), line[0], line[1], roadWidth)

			# Draw the taxi
			taxi.draw(screen)
			if taxi.is_on_grass(screen):
				pass

		# Always update the display at the end of the loop
		pygame.display.update()