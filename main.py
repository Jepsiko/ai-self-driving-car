import pygame
import math
from Car import Car

WIDTH = 1366
HEIGHT = 768
MIN_DIST_POINTS = 150
DEBUG = False


def draw_line(screen, line, color, width):
	pos1, pos2 = line
	x1, y1 = pos1
	x2, y2 = pos2
	length = math.hypot(x1 - x2, y1 - y2)
	angle = math.acos((x2-x1)/length)
	if y2 < y1:
		angle = math.pi*2 - angle
	point1 = (x1 + int(width/2 * math.cos(angle+math.pi/2)), y1 + int(width/2 * math.sin(angle+math.pi/2)))
	point2 = (x1 + int(width/2 * math.cos(angle-math.pi/2)), y1 + int(width/2 * math.sin(angle-math.pi/2)))
	point3 = (x2 + int(width/2 * math.cos(angle-math.pi/2)), y2 + int(width/2 * math.sin(angle-math.pi/2)))
	point4 = (x2 + int(width/2 * math.cos(angle+math.pi/2)), y2 + int(width/2 * math.sin(angle+math.pi/2)))
	pygame.draw.polygon(screen, color, [point1, point2, point3, point4])


def ccw(A, B, C):
	return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def is_line_crossing(line1, line2):
	A, B = line1
	C, D = line2

	# Prevent lines starting from the same point from being noticed as crossed lines
	if A == C or A == D or B == C or B == D:
		return False

	return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)


if __name__ == "__main__":
	print("Press P to edit points, L to edit lines, F when you've finished and D for debug")

	# Initialize pygame
	pygame.init()

	# Create the screen
	screen = pygame.display.set_mode((WIDTH, HEIGHT))

	# Title and Icon
	pygame.display.set_caption("Taxi Agent")
	icon = pygame.image.load("taxi.png")
	pygame.display.set_icon(icon)

	# Taxi taxi
	taxi = Car("car.png", 0, 0)

	# Level creation
	pointEditing = True
	lineEditing = False
	startingPoint = None
	endingPoint = None
	crossing = False
	points = []
	lines = []

	# Level design
	roadColor = (100, 100, 100)
	roadWidth = 50

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

						# Line creation
						mouseX, mouseY = pygame.mouse.get_pos()
						for position in points:
							if math.hypot(position[0] - mouseX, position[1] - mouseY) <= 40:
								if startingPoint is None:
									startingPoint = position
								elif position != startingPoint and not crossing:
									endingPoint = position

				if event.button == 3:

					# Point removing
					if pointEditing:
						mouseX, mouseY = pygame.mouse.get_pos()
						position_to_remove = None
						for position in points:
							if math.hypot(position[0] - mouseX, position[1] - mouseY) <= 40:
								removePos = position
								position_to_remove = position
								break

						# Remove the point and all lines connected to it
						if position_to_remove is not None:
							points.remove(position_to_remove)
							for line in reversed(lines):
								if position_to_remove in line:
									lines.remove(line)

					# Cancel the new line drawing
					if lineEditing:
						startingPoint = None

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

				# Finished mode
				if event.key == pygame.K_f:
					taxi.position[0], taxi.position[1] = points[0]

					lineEditing = False
					pointEditing = False

				# Debug mode
				if event.key == pygame.K_d:
					DEBUG = not DEBUG

		# Change the background color
		screen.fill((0, 50, 0))

		# Level editing GUI
		mouseX, mouseY = pygame.mouse.get_pos()
		if pointEditing:

			spaceAvailable = True
			for position in points:
				radius = MIN_DIST_POINTS
				transparent_circle = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
				pygame.draw.circle(transparent_circle, (150, 150, 150, 50), (radius*2, radius*2), radius-2)
				pygame.draw.circle(transparent_circle, (200, 200, 200, 50), (radius*2, radius*2), radius, 2)
				screen.blit(transparent_circle, (position[0] - radius*2, position[1] - radius*2))
				pygame.draw.circle(screen, (100, 150, 255), position, 10)

				if math.hypot(position[0] - mouseX, position[1] - mouseY) <= MIN_DIST_POINTS:
					spaceAvailable = False

			if pygame.mouse.get_focused():
				if spaceAvailable:
					pygame.draw.circle(screen, (150, 150, 150), (mouseX, mouseY), 8)
					pygame.draw.circle(screen, (200, 200, 200), (mouseX, mouseY), 10, 2)
				else:
					pygame.draw.circle(screen, (150, 100, 100), (mouseX, mouseY), 8)
					pygame.draw.circle(screen, (200, 150, 150), (mouseX, mouseY), 10, 2)

				# Add a new point
				if pygame.mouse.get_pressed()[0] and spaceAvailable:
					points.append((mouseX, mouseY))

		elif lineEditing:
			for position in points:
				radius = int(roadWidth/2)
				transparent_circle = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
				pygame.draw.circle(transparent_circle, (150, 150, 150, 50), (radius, radius), radius-2)
				pygame.draw.circle(transparent_circle, (200, 200, 200, 50), (radius, radius), radius, 2)
				screen.blit(transparent_circle, (position[0] - radius, position[1] - radius))
				pygame.draw.circle(screen, (100, 100, 100), position, 10)

			crossing = False
			for line in lines:
				draw_line(screen, line, (100, 100, 100), 20)

				if startingPoint is not None and is_line_crossing(line, (startingPoint, (mouseX, mouseY))):
					crossing = True

			if startingPoint is not None:
				line_to_mouse = (startingPoint, (mouseX, mouseY))
				if crossing:
					draw_line(screen, line_to_mouse, (150, 100, 100), 20)
				else:
					draw_line(screen, line_to_mouse, (100, 100, 100), 20)

			# Add a new line
			if endingPoint is not None:
				lines.append([startingPoint, endingPoint])

				startingPoint = None
				endingPoint = None

		else:
			# Draw the map
			radius = int(roadWidth/2)
			for position in points:
				pygame.draw.circle(screen, roadColor, position, radius)

			for line in lines:
				draw_line(screen, line, roadColor, roadWidth)

			# Draw the taxi
			taxi.draw(screen)
			if taxi.is_on_grass(screen):
				pass

		# Always update the display at the end of the loop
		pygame.display.update()
