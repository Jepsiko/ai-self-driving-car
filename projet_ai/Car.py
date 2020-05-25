import pygame
from pygame import Vector2
import math
import numpy as np
from projet_ai import Event, Tools


class Lidar(Event.Listener):

	def __init__(self, evManager, row=5, col=5, width=180, length=150, back_length=50):
		super().__init__(evManager)

		self.row = row
		self.col = col
		self.matrix = np.zeros((row, col), dtype=int)
		self.width = width
		self.length = length
		self.back_length = back_length
		self.map = None

	def notify(self, event):
		if isinstance(event, Event.MapUpdatedEvent):
			self.map = event.map

		elif isinstance(event, Event.CarUpdatedEvent):
			self.update(event.car.position, event.car.angle)

	def update(self, position, angle):
		if self.map is None:
			return

		angle = -angle

		vec = Vector2()
		vec.from_polar((self.length - self.back_length, angle))
		front = position + vec

		vec.from_polar((self.width / 2, angle - 90))
		front_left = front + vec

		current = front_left

		for i in range(len(self.matrix)):
			first_of_line = Vector2(current)
			for j in range(len(self.matrix[i])):
				if self.map.is_point_on_road(current):
					self.matrix[i][j] = 1
				else:
					self.matrix[i][j] = 0

				vec.from_polar((self.width / (self.col - 1), angle + 90))
				current += vec
			vec.from_polar((self.length / (self.row - 1), angle + 180))
			current = first_of_line + vec


class Car(Event.Listener):

	def __init__(self, img, evManager):
		super().__init__(evManager)
		self.image = pygame.image.load(img)
		self.width = self.image.get_rect().height
		self.length = self.image.get_rect().width

		self.position = Vector2(0, 0)
		self.lidar = Lidar(evManager, 7, 6)

		self.direction = Vector2(0, 0)

		self.angle = 0
		self.acceleration = 0
		self.steering = 0
		self.velocity = Vector2(0, 0)

		self.max_acceleration = 50
		self.max_steering = 40
		self.max_velocity = 160

		self.brake_deceleration = 90
		self.free_deceleration = 30

		self.map = None

	def notify(self, event):
		if isinstance(event, Event.MovePlayerEvent):
			self.direction = event.direction

		elif isinstance(event, Event.TickEvent):
			if self.direction.x == 1:
				if self.velocity.x < 0:
					self.acceleration = self.brake_deceleration
				else:
					self.acceleration = self.max_acceleration * self.direction.x
			elif self.direction.x == -1:
				if self.velocity.x > 0:
					self.acceleration = -self.brake_deceleration
				else:
					self.acceleration = self.max_acceleration * self.direction.x
			else:
				if abs(self.velocity.x) > event.delta * self.free_deceleration:
					self.acceleration = -math.copysign(self.free_deceleration, self.velocity.x)
				else:
					if event.delta != 0:
						self.acceleration = -self.velocity.x / event.delta
			self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))

			self.steering = self.max_steering * self.direction.y
			self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

			self.velocity += (self.acceleration * event.delta, 0)
			self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

			if self.steering:
				turn_rad = self.length / math.sin(math.radians(self.steering))
				velocity_angle = self.velocity.x / turn_rad
			else:
				velocity_angle = 0

			self.position += self.velocity.rotate(-self.angle) * event.delta
			self.angle += math.degrees(velocity_angle) * event.delta

			self.evManager.post(Event.CarUpdatedEvent(self))

		elif isinstance(event, Event.MapUpdatedEvent):
			self.map = event.map

	def from_angle(self, angle):
		rads = math.radians(angle)
		self.direction = Vector2(math.sin(rads), math.cos(rads))

	def from_vector(self, vector):
		self.direction = (vector - self.position).normalize()

	def get_state(self):
		return self.lidar.matrix

	def set_position(self, position):
		self.position = position
		self.evManager.post(Event.CarUpdatedEvent(self))

	def get_hitbox(self):
		angle = -self.angle
		vec = Vector2()

		vec.from_polar((self.length / 2, angle))
		front = self.position + vec

		vec.from_polar((self.width / 2, angle + 90))
		front_right = front + vec
		vec.from_polar((self.width / 2, angle - 90))
		front_left = front + vec

		vec.from_polar((self.length / 2, angle + 180))
		back = self.position + vec

		vec.from_polar((self.width / 2, angle + 90))
		back_right = back + vec
		vec.from_polar((self.width / 2, angle - 90))
		back_left = back + vec

		return [front_left, front_right, back_right, back_left]

	def is_on_road(self):
		if self.map is None:
			return False

		for point in self.get_hitbox():
			if not self.map.is_point_on_road(point):
				return False
		return True
