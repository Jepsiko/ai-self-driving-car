import pygame
import Event
import math
import Settings
import Tools


class Graph:

	def __init__(self, points, lines):
		self.pointNumber = {}  # Assiociate each point with a number for the matrix
		for i in range(len(points)):
			self.pointNumber[points[i]] = i
		self.adjacencyMatrix = [[math.inf for _ in points] for _ in points]

		for line in lines:
			pos1, pos2 = line
			distance = math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1])

			self.adjacencyMatrix[self.pointNumber[pos1]][self.pointNumber[pos2]] = distance
			self.adjacencyMatrix[self.pointNumber[pos2]][self.pointNumber[pos1]] = distance

	def get_points(self):
		return self.pointNumber.keys()

	def get_distance(self, point1, point2):
		distance = self.adjacencyMatrix[self.pointNumber[point1]][self.pointNumber[point2]]
		return distance if distance != math.inf else None


class Map(Event.Listener):

	def __init__(self, evManager):
		super().__init__(evManager)

		self.firstPoint = None
		self.crossing = False

		self.points = []
		self.lines = []

		self.graph = None

	def build(self):
		self.graph = Graph(self.points, self.lines)
		self.post(Event.MapUpdatedEvent(self))
		return self.graph

	def create_point(self):
		# Add a new point
		mouse = pygame.mouse.get_pos()
		if self.is_space_available(mouse):
			self.points.append(mouse)

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

	def remove_point(self):
		# Remove the point and all lines connected to it
		mouse = pygame.mouse.get_pos()
		point_to_remove = self.get_point_selected(mouse)

		if point_to_remove is not None:
			self.points.remove(point_to_remove)

			for line in reversed(self.lines):
				if point_to_remove in line:
					self.lines.remove(line)

	def cancel_line(self):
		self.firstPoint = None

	def get_building_line(self):
		return [self.firstPoint, pygame.mouse.get_pos()] if self.firstPoint is not None else None

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
			if math.hypot(point[0] - mouse[0], point[1] - mouse[1]) <= Settings.MIN_DIST_POINTS:
				return False
		return True

	def get_point_selected(self, mouse):
		for point in self.points:
			if Map.is_point_selected(point, mouse):
				return point
		return None

	@staticmethod
	def is_point_selected(point, mouse):
		return math.hypot(point[0] - mouse[0], point[1] - mouse[1]) <= Settings.DIST_SELECT_POINT
