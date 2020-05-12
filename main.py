import pygame
from Car import Car
from Graph import Graph
import settings
from tools import *
from GameUI import GameUI


def create_reward_gates():
	gatesWidth = settings.ROAD_WIDTH - 4
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
			pointLeft = (int(pointMiddle[0] + gatesWidth / 2 * math.cos(angle - math.pi / 2)),
						 int(pointMiddle[1] + gatesWidth / 2 * math.sin(angle - math.pi / 2)))
			pointRight = (int(pointMiddle[0] + gatesWidth / 2 * math.cos(angle + math.pi / 2)),
						  int(pointMiddle[1] + gatesWidth / 2 * math.sin(angle + math.pi / 2)))
			rewardGates[i].append((pointLeft, pointRight))


if __name__ == "__main__":

	print("Press P to edit points, L to edit lines, F when you've finished, D for debug and ESC to quit")

	# Initialize pygame
	pygame.init()

	gameUI = GameUI()

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
					# create_reward_gates()  # TODO: maybe no use for it

				# "D" to enter Debug mode
				if event.key == pygame.K_d:
					settings.DEBUG = not settings.DEBUG

				# "ESC" to Quit
				if event.key == pygame.K_ESCAPE:
					running = False

		# Change the background color
		gameUI.draw_background()

		# Level editing GUI
		if pointEditing:
			gameUI.point_editing(points)
		elif lineEditing:
			startingPoint, endingPoint = gameUI.line_editing(points, lines, startingPoint, endingPoint)
		else:
			gameUI.draw_game(points, lines, taxi)

		# Always update the display at the end of the loop
		pygame.display.update()
