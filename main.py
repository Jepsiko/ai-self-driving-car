import pygame
import math
from Car import Car
from Graph import Graph


def draw_line(screen, line, color, width):
	pos1, pos2 = line
	x1, y1 = pos1
	x2, y2 = pos2
	length = math.hypot(x1 - x2, y1 - y2)
	angle = math.acos((x2 - x1) / length)
	if y2 < y1:
		angle = math.pi * 2 - angle
	point1 = (x1 + int(width / 2 * math.cos(angle + math.pi / 2)), y1 + int(width / 2 * math.sin(angle + math.pi / 2)))
	point2 = (x1 + int(width / 2 * math.cos(angle - math.pi / 2)), y1 + int(width / 2 * math.sin(angle - math.pi / 2)))
	point3 = (x2 + int(width / 2 * math.cos(angle - math.pi / 2)), y2 + int(width / 2 * math.sin(angle - math.pi / 2)))
	point4 = (x2 + int(width / 2 * math.cos(angle + math.pi / 2)), y2 + int(width / 2 * math.sin(angle + math.pi / 2)))
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


def create_reward_gates():
	for i in range(len(lines)):
		pos1, pos2 = lines[i]
		x1, y1 = pos1
		x2, y2 = pos2
		length = math.hypot(x1 - x2, y1 - y2)
		angle = math.acos((x2 - x1) / length)
		if y2 < y1:
			angle = math.pi * 2 - angle

		rewardGates.append([])
		for j in range(spaceBetweenGates, int(length) - spaceBetweenGates, spaceBetweenGates):
			pointMiddle = (x1 + j * math.cos(angle), y1 + j * math.sin(angle))
			pointLeft = (int(pointMiddle[0] + roadWidth / 2 * math.cos(angle - math.pi / 2)),
						 int(pointMiddle[1] + roadWidth / 2 * math.sin(angle - math.pi / 2)))
			pointRight = (int(pointMiddle[0] + roadWidth / 2 * math.cos(angle + math.pi / 2)),
						  int(pointMiddle[1] + roadWidth / 2 * math.sin(angle + math.pi / 2)))
			rewardGates[i].append((pointLeft, pointRight))


if __name__ == "__main__":
	WIDTH = 1366
	HEIGHT = 768
	DEBUG = False

	print("Press P to edit points, L to edit lines, F when you've finished, D for debug and ESC to quit")

	# Initialize pygame
	pygame.init()

	# Create the screen
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	# screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN) #  For the final version

	# Title and Icon
	pygame.display.set_caption("Taxi Agent")
	icon = pygame.image.load("taxi.png")
	pygame.display.set_icon(icon)

	# Taxi taxi
	taxi = Car("car.png", 0, 0)

	# Level creation
	minimalDistancePoint = 150
	pointEditing = True
	lineEditing = False
	startingPoint = None
	endingPoint = None
	crossing = False
	points = []
	lines = []

	# Level design
	backgroundColor = (20, 60, 20)
	roadColor = (100, 100, 100)
	roadWidth = 50

	# Reward gates
	rewardGates = []
	spaceBetweenGates = 50

	# Graph creation
	graph = None

	# Game Loop
	running = True
	while running:

		# Event handling
		for event in pygame.event.get():

			# If the red cross in the upper right corner is clicked
			if event.type == pygame.QUIT:
				running = False

			if event.type == pygame.MOUSEBUTTONDOWN:

				# Left clic
				if event.button == 1:

					# Line creation
					if lineEditing:
						mouseX, mouseY = pygame.mouse.get_pos()
						for position in points:
							if math.hypot(position[0] - mouseX, position[1] - mouseY) <= 40:
								if startingPoint is None:
									startingPoint = position
								elif position != startingPoint and not crossing:
									endingPoint = position

				# Right clic
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

				# "P" to enter Point editing mode
				if event.key == pygame.K_p:
					pointEditing = True
					lineEditing = False
					graph = None
					rewardGates = []

				# "L" to enter Line editing mode
				if event.key == pygame.K_l:
					lineEditing = True
					pointEditing = False
					graph = None
					rewardGates = []

				# "F" to Finish editing
				if event.key == pygame.K_f:
					if len(points) > 0:
						taxi.position[0], taxi.position[1] = points[0]

					lineEditing = False
					pointEditing = False
					graph = Graph(points, lines)
					create_reward_gates()

				# "D" to enter Debug mode
				if event.key == pygame.K_d:
					DEBUG = not DEBUG

				# "ESC" to Quit
				if event.key == pygame.K_ESCAPE:
					running = False

		# Change the background color
		screen.fill(backgroundColor)

		# Level editing GUI
		mouseX, mouseY = pygame.mouse.get_pos()
		if pointEditing:

			spaceAvailable = True
			for position in points:
				radius = minimalDistancePoint
				transparent_circle = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
				pygame.draw.circle(transparent_circle, (150, 150, 150, 50), (radius * 2, radius * 2), radius - 2)
				pygame.draw.circle(transparent_circle, (200, 200, 200, 50), (radius * 2, radius * 2), radius, 2)
				screen.blit(transparent_circle, (position[0] - radius * 2, position[1] - radius * 2))
				pygame.draw.circle(screen, (100, 150, 255), position, 10)

				if math.hypot(position[0] - mouseX, position[1] - mouseY) <= minimalDistancePoint:
					spaceAvailable = False

			# If the mouse is in the window
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
				radius = int(roadWidth / 2)
				transparent_circle = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
				pygame.draw.circle(transparent_circle, (150, 150, 150, 50), (radius, radius), radius - 2)
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

		# Level out of editing mode
		else:
			# Draw the roads
			radius = int(roadWidth / 2)
			for position in points:
				pygame.draw.circle(screen, roadColor, position, radius)

			for line in lines:
				draw_line(screen, line, roadColor, roadWidth)

			# Draw the reward gates
			colorRewardGates = (101, 101, 101)
			if DEBUG:
				colorRewardGates = (255, 0, 0)
			for road in rewardGates:
				for line in road:
					if DEBUG:
						pygame.draw.line(screen, colorRewardGates, line[0], line[1], 2)

			# Draw the taxi
			taxi.draw(screen)
			if taxi.is_on_grass(screen, backgroundColor):
				pass

		# Always update the display at the end of the loop
		pygame.display.update()
