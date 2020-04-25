import math


class Graph:

	def __init__(self, points, lines):
		self.pointNumber = {}
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
