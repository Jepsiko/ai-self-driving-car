import pygame
from pygame.locals import *
import math
from Car import Car
from Graph import Graph
import settings
from tools import *
from GameUI import GameUI

def on_press(direction, vect):
	keys_pressed = pygame.key.get_pressed()

	if direction:
		if direction == K_UP:
			vect[1]-=1

		elif direction == K_DOWN:
			vect[1]+=1

		if direction == K_LEFT:
			vect[0]-=1

		elif direction == K_RIGHT:
			vect[0]+=1

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

	#Keyboard
	UP='up'
	LEFT='left'
	RIGHT='right'
	DOWN='down'
	direction=None

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
		else :
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
					pygame.draw.line(screen, colorRewardGates, line[0], line[1], 2)

			# Draw the taxi
			taxi.draw(screen)
			if taxi.is_on_grass(screen, backgroundColor):
				pass
			else :
				for event in pygame.event.get():
						if event.type == KEYDOWN:
								direction = event.key
						if event.type == KEYUP:
								if (event.key == direction):
										direction = None
				on_press(direction, taxi.get_position())
				taxi.move()

			startingPoint, endingPoint = gameUI.line_editing(points, lines, startingPoint, endingPoint)
		else:
			gameUI.game(points, lines)

		# Always update the display at the end of the loop
		pygame.display.update()
