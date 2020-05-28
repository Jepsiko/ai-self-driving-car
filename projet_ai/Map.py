import pygame
import math
from projet_ai import Tools, Event, Settings
from pygame import Vector2
import random


class Node(Vector2):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.reset()

	def reset(self):
		self.g = 0
		self.h = 0
		self.parent = None

	def f(self):
		return self.g + self.h

	def to_coord(self):
		return int(self.x), int(self.y)

	@staticmethod
	def from_coord(point):
		return Node(point[0], point[1])

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y


class Map(Event.Listener):

	def __init__(self, evManager):
		super().__init__(evManager)

		self.reset()

	def notify(self, event):
		if isinstance(event, Event.SaveMapEvent):
			self.save_map(event.map_name)

		elif isinstance(event, Event.UpdatePathEvent):
			self.update_path()

	def reset(self):

		self.firstPoint = None
		self.crossing = False

		self.points = []
		self.lines = []

		self.path = None

	def get_point(self, i):
		if i < len(self.points):
			return self.points[i]
		else:
			return None

	@staticmethod
	def get_distance(pos1, pos2):
		return math.hypot(pos1.x - pos2.x, pos1.y - pos2.y)

	def get_neighbours(self, point):
		neighbours = []
		for line in self.lines:
			if point == line[0]:
				neighbours.append(line[1])
			elif point == line[1]:
				neighbours.append(line[0])
		return neighbours

	def create_path(self):
		start = random.choice(self.points)
		neighbour = random.choice(self.get_neighbours(start))
		ends = self.get_neighbours(neighbour)
		ends.remove(start)
		self.path = [start, neighbour, random.choice(ends)]

	def update_path(self):
		self.path[0] = self.path[1]
		self.path[1] = self.path[2]
		neighbours = self.get_neighbours(self.path[1])
		neighbours.remove(self.path[0])
		self.path[2] = random.choice(neighbours)

	@staticmethod
	def is_point_in_rectangle(point, rectangle):
		P = point
		A, B, C, D = rectangle
		AP = Vector2(P.x - A.x, P.y - A.y)
		AB = Vector2(B.x - A.x, B.y - A.y)
		AD = Vector2(D.x - A.x, D.y - A.y)

		return 0 < AP.dot(AB) < AB.dot(AB) and 0 < AP.dot(AD) < AD.dot(AD)

	@staticmethod
	def get_rect(line, width):
		X, Y = line

		length = X.distance_to(Y)
		if length == 0:
			return None

		angle = math.degrees(math.atan2(Y.y - X.y, Y.x - X.x))
		if angle < 0:
			angle += 360

		vec = Vector2()
		vec.from_polar((width / 2, angle + 90))
		A = X + vec

		vec.from_polar((width / 2, angle - 90))
		B = X + vec

		vec.from_polar((width / 2, angle - 90))
		C = Y + vec

		vec.from_polar((width / 2, angle + 90))
		D = Y + vec

		return [A, B, C, D]

	def create_point(self):
		# Add a new point
		mouse = pygame.mouse.get_pos()
		if self.is_space_available(mouse):
			self.points.append(Node.from_coord(mouse))

			self.evManager.post(Event.MapUpdatedEvent(self))

	def create_line(self):
		for point in self.points:
			mouse = pygame.mouse.get_pos()
			if Map.is_point_selected(point, mouse):

				# First point selected
				if self.firstPoint is None:
					self.firstPoint = point

				# Second point selected
				elif point != self.firstPoint and not self.is_crossing(self.get_building_line()):

					# Creation of a new line
					self.lines.append([self.firstPoint, point])
					self.firstPoint = None
					self.evManager.post(Event.MapUpdatedEvent(self))

	def remove_point(self):
		# Remove the point and all lines connected to it
		mouse = pygame.mouse.get_pos()
		point_to_remove = self.get_point_selected(mouse)

		if point_to_remove is not None:
			self.points.remove(point_to_remove)

			for line in reversed(self.lines):
				if point_to_remove in line:
					self.lines.remove(line)

			self.evManager.post(Event.MapUpdatedEvent(self))

	def cancel_line(self):
		self.firstPoint = None

	def get_building_line(self):
		mouse = pygame.mouse.get_pos()
		return [self.firstPoint, Node.from_coord(mouse)] if self.firstPoint is not None else None

	def is_crossing(self, line):
		for road in self.lines:
			if Tools.is_line_crossing(road, line):
				return True
		return False

	def is_space_available(self, mouse):
		# If the mouse is out of the screen
		if not pygame.mouse.get_focused():
			return False

		for point in self.points:
			if math.hypot(point.x - mouse[0], point.y - mouse[1]) <= Settings.MIN_DIST_POINTS:
				return False
		return True

	def get_point_selected(self, mouse):
		for point in self.points:
			if Map.is_point_selected(point, mouse):
				return point
		return None

	@staticmethod
	def is_point_selected(point, mouse):
		return math.hypot(point.x - mouse[0], point.y - mouse[1]) <= Settings.DIST_SELECT_POINT

	def is_point_on_last_road(self, point):
		if self.path is not None:
			return Map.is_point_in_rectangle(point, Map.get_rect([self.path[-1], self.path[-2]], Settings.ROAD_WIDTH))
		else:
			return False

	def is_point_on_road(self, point):
		for road in self.lines:
			A, B = road

			if Map.is_point_in_rectangle(point, Map.get_rect(road, Settings.ROAD_WIDTH)):
				return True

			if point.distance_to(A) <= Settings.ROAD_WIDTH/2:
				return True

			if point.distance_to(B) <= Settings.ROAD_WIDTH/2:
				return True

		return False

	def is_point_on_path(self, point):
		if self.path is None:
			return False

		for i in range(len(self.path)-1):
			A = self.path[i]
			B = self.path[i+1]

			if Map.is_point_in_rectangle(point, Map.get_rect([A, B], Settings.ROAD_WIDTH)):
				return True

			if point.distance_to(A) <= Settings.ROAD_WIDTH/2:
				return True

			if point.distance_to(B) <= Settings.ROAD_WIDTH/2:
				return True

		return False

	def save_map(self, name):
		with open(name, 'w') as file:
			for point in self.points:
				file.write(str(int(point.x)) + ',' + str(int(point.y)) + ' ')
			file.write('\n')
			for line in self.lines:
				for point in line:
					file.write(str(int(point.x)) + ',' + str(int(point.y)) + ' ')
				file.write('\n')

	def load_map(self, name):
		self.reset()

		with open(name, 'r') as file:
			for point in file.readline().split(' ')[:-1]:
				point = point.split(',')
				point = Node(int(point[0]), int(point[1]))
				self.points.append(point)

			for line in file.readlines():
				new_line = []
				for point in line.split(' ')[:-1]:
					point = point.split(',')
					point = Node(int(point[0]), int(point[1]))
					new_line.append(point)
				self.lines.append(new_line)

		self.evManager.post(Event.MapUpdatedEvent(self))
