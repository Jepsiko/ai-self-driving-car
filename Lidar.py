import pygame
import math
import numpy as np
from pygame.math import Vector2


def get_point_at_vector(pos, magnitude, angle):
	return Vector2(pos.x + magnitude * math.cos(angle), pos.y + magnitude * math.sin(angle))


class Lidar:

	def __init__(self, lin=5, col=5, width=200, length=150, back_length=50):

		self.matrix = np.zeros((lin, col), dtype=int)
		self.width = width
		self.length = length
		self.back_length = back_length

	def update(self, pos, angle):
		self.matrix[6][2] = 99
		for i in range(len(self.matrix)):
			for j in range(len(self.matrix[i])):
				pass
				# print(self.matrix[i][j])

		# print(self.matrix)

	def draw(self, screen, pos, angle):

		front = get_point_at_vector(pos, self.length - self.back_length, angle)
		front_left = get_point_at_vector(front, self.width / 2, math.pi / 2 + angle)
		front_right = get_point_at_vector(front, self.width / 2, angle - math.pi / 2)

		back = get_point_at_vector(pos, self.back_length, math.pi + angle)
		back_left = get_point_at_vector(back, self.width / 2, math.pi / 2 + angle)
		back_right = get_point_at_vector(back, self.width / 2, angle - math.pi / 2)

		lidar_points = [front_left, back_left, back_right, front_right]
		pygame.draw.lines(screen, (200, 0, 0), True, lidar_points)

		# self.draw_circle(frontleft, back_left, frontright, self.width, self.length + self.back_length)

	def draw_circle(self, frontofleft, behindleft, frontofright, width, lenght):
		lin = self.matrix

		pass
