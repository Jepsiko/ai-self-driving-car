import numpy as np
import math
from projet_ai import Settings, Tools


class Lidar:

	def __init__(self, row=5, col=5, width=180, length=150, back_length=50):

		self.row = row
		self.col = col
		self.matrix = np.zeros((row, col), dtype=int)
		self.width = width
		self.length = length
		self.back_length = back_length

	def update(self, screen, pos, angle):
		front = Tools.get_point_at_vector(pos, self.length - self.back_length, angle)
		front_left = Tools.get_point_at_vector(front, self.width / 2, angle - math.pi / 2)

		current = front_left

		for i in range(len(self.matrix)):
			first_of_line = current
			for j in range(len(self.matrix[i])):
				try:
					color_current = screen.get_at((int(current.x), int(current.y)))
				except IndexError:  # If the current point is out of the screen
					color_current = Settings.GRASS_COLOR

				if color_current == Settings.GRASS_COLOR:
					self.matrix[i][j] = 0
				elif color_current == Settings.ROAD_COLOR:
					self.matrix[i][j] = 1
				else:
					self.matrix[i][j] = 1

				current = Tools.get_point_at_vector(current, self.width / (self.col - 1), math.pi / 2 + angle)
			current = Tools.get_point_at_vector(first_of_line, self.length / (self.row - 1), math.pi + angle)
