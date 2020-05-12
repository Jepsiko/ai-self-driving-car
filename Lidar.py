import pygame
import math
import numpy as np
from pygame.math import Vector2


def get_point_at_vector(pos, magnitude, angle):
	return Vector2(pos.x + magnitude * math.cos(angle), pos.y + magnitude * math.sin(angle))


class Lidar:

	def __init__(self, row=5, col=5, width=180, length=150, back_length=50):

		self.row = row
		self.col = col
		self.matrix = np.zeros((row, col), dtype=int)
		self.width = width
		self.length = length
		self.back_length = back_length

	def update(self, screen, pos, angle):
		front = get_point_at_vector(pos, self.length - self.back_length, angle)
		front_left = get_point_at_vector(front, self.width / 2, angle - math.pi / 2)

		current = front_left

		for i in range(len(self.matrix)):
			first_of_line = current
			for j in range(len(self.matrix[i])):
				color_current = screen.get_at((int(current.x), int(current.y)))

				if color_current == (0, 100, 0):
					self.matrix[i][j] = 0
				elif color_current == (100, 100, 100):
					self.matrix[i][j] = 1
				else:
					self.matrix[i][j] = 1

				current = get_point_at_vector(current, self.width / (self.col - 1), math.pi / 2 + angle)
			current = get_point_at_vector(first_of_line, self.length / (self.row - 1), math.pi + angle)

	def draw(self, screen, pos, angle):

		front = get_point_at_vector(pos, self.length - self.back_length, angle)
		front_right = get_point_at_vector(front, self.width / 2, math.pi / 2 + angle)
		front_left = get_point_at_vector(front, self.width / 2, angle - math.pi / 2)

		back = get_point_at_vector(pos, self.back_length, math.pi + angle)
		back_right = get_point_at_vector(back, self.width / 2, math.pi / 2 + angle)
		back_left = get_point_at_vector(back, self.width / 2, angle - math.pi / 2)

		lidar_corners = [front_left, back_left, back_right, front_right]
		pygame.draw.lines(screen, (200, 0, 0), True, lidar_corners)

		self.draw_lidar_points(screen, pos, angle)

	def draw_lidar_points(self, screen, pos, angle):

		front = get_point_at_vector(pos, self.length - self.back_length, angle)
		front_left = get_point_at_vector(front, self.width / 2, angle - math.pi / 2)

		current = front_left

		for i in range(len(self.matrix)):
			first_of_line = current
			for j in range(len(self.matrix[i])):
				pygame.draw.circle(screen, (0, 255, 0), (int(current.x), int(current.y)), 3)

				current = get_point_at_vector(current, self.width / (self.col - 1), math.pi / 2 + angle)
			current = get_point_at_vector(first_of_line, self.length / (self.row - 1), math.pi + angle)

	def draw_view(self, screen, pos):
		x, y = pos
		border_size = 5
		square_size = 15

		border = pygame.rect.Rect(x, y,
								  self.col * square_size + border_size * 2,
								  self.row * square_size + border_size * 2)
		pygame.draw.rect(screen, (0, 0, 0), border)
		x += border_size
		y += border_size
		for i in range(self.row):
			for j in range(self.col):
				square = pygame.rect.Rect(j*square_size + x, i*square_size + y, square_size, square_size)

				if self.matrix[i][j] == 0:
					pygame.draw.rect(screen, (0, 150, 0), square)
				else:
					pygame.draw.rect(screen, (100, 100, 100), square)
