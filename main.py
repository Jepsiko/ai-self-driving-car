import pygame
from Graph import Graph
import settings
from tools import *
from GameUI import GameUI


if __name__ == "__main__":

	print("Press P to edit points, L to edit lines, F when you've finished, D for debug and ESC to quit")

	# Initialize pygame
	pygame.init()

	gameUI = GameUI()

	# Level creation
	pointEditing = True
	lineEditing = False
	startingPoint = None
	endingPoint = None
	crossing = False
	points = []
	lines = []

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

				# "L" to enter Line editing mode
				if event.key == pygame.K_l:
					lineEditing = True
					pointEditing = False
					graph = None

				# "F" to Finish editing
				if event.key == pygame.K_f:
					if len(points) > 0:
						gameUI.change_car_position(Vector2(points[0]))

					lineEditing = False
					pointEditing = False
					graph = Graph(points, lines)

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
			gameUI.game(points, lines)

		# Always update the display at the end of the loop
		pygame.display.update()
