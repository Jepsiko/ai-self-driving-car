import pygame
import math
import numpy as np
from pygame.math import Vector2


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

		front = Vector2(pos.x + (self.length - self.back_length) * math.cos(angle),
						pos.y + (self.length - self.back_length) * math.sin(angle))
		front_left = Vector2(front.x + self.width / 2 * math.cos(math.pi / 2 + angle),
							 front.y + self.width / 2 * math.sin(math.pi / 2 + angle))
		front_right = Vector2(front.x + self.width / 2 * math.cos(angle - math.pi / 2),
							  front.y + self.width / 2 * math.sin(angle - math.pi / 2))

		back = Vector2(pos.x + self.back_length * math.cos(math.pi + angle),
					   pos.y + self.back_length * math.sin(math.pi + angle))
		back_left = Vector2(back.x + self.width / 2 * math.cos(math.pi / 2 + angle),
					 		back.y + self.width / 2 * math.sin(math.pi / 2 + angle))
		back_right = Vector2(back.x + self.width / 2 * math.cos(angle - math.pi / 2),
							 back.y + self.width / 2 * math.sin(angle - math.pi / 2))

		lidar_points = [front_left, back_left, back_right, front_right]
		pygame.draw.lines(screen, (200, 0, 0), True, lidar_points)

		# self.draw_circle(frontleft, back_left, frontright, self.width, self.length + self.back_length)

	def draw_circle(self, frontofleft, behindleft, frontofright, width, lenght):
		lin = self.matrix

		pass
