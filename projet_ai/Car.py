import pygame
from pygame import Vector2
import math
import numpy as np
from projet_ai import Event


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
		self.angle = 0

		self.direction = Vector2(0, 0)

		self.acceleration = 0
		self.steering = 0
		self.velocity = Vector2(0, 0)

		self.max_acceleration = 50
		self.max_steering = 40
		self.max_front_velocity = 180
		self.max_rear_velocity = 50

		self.brake_deceleration = 120
		self.free_deceleration = 30

		self.lidar = Lidar(evManager, 7, 6)

		self.map = None

	def display_info(self):
		print('--- Car ---')
		print('Position :', self.position)
		print('Direction :', self.direction)
		print('Velocity :', self.velocity)
		print('Angle :', self.angle)
		print('Acceleration :', self.acceleration)
		print('Steering :', self.steering)

	def notify(self, event):
		if isinstance(event, Event.MovePlayerEvent):
			self.direction = event.direction

		elif isinstance(event, Event.TickEvent):
			if (self.direction.x > 0 and self.velocity.x < 0) or (self.direction.x < 0 and self.velocity.x > 0):
				self.acceleration = self.brake_deceleration
			elif self.direction.x != 0:
				self.acceleration = self.max_acceleration * self.direction.x
			else:
				if abs(self.velocity.x) > event.delta * self.free_deceleration:
					self.acceleration = -math.copysign(self.free_deceleration, self.velocity.x)
				else:
					if event.delta != 0:
						self.acceleration = -self.velocity.x / event.delta

			self.steering = self.max_steering * self.direction.y

			self.velocity += (self.acceleration * event.delta, 0)
			self.velocity.x = max(-self.max_rear_velocity, min(self.velocity.x, self.max_front_velocity))

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

	def get_number_inputs(self):
		return self.lidar.row * self.lidar.col + 3

	def get_state(self):
		lidar_size = self.lidar.row * self.lidar.col
		state = self.lidar.matrix.reshape(lidar_size)
		state = np.append(state, self.acceleration / self.max_acceleration)
		state = np.append(state, self.steering / self.max_steering)
		state = np.append(state, self.velocity.x / self.max_front_velocity)
		return state

	def reset(self, position, angle):
		self.position = position
		self.angle = angle

		self.direction = Vector2(0, 0)

		self.acceleration = 0
		self.steering = 0
		self.velocity = Vector2(0, 0)

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
		rear = self.position + vec

		vec.from_polar((self.width / 2, angle + 90))
		rear_right = rear + vec
		vec.from_polar((self.width / 2, angle - 90))
		rear_left = rear + vec

		return [front_left, front_right, rear_right, rear_left]

	def is_on_road(self):
		if self.map is None:
			return False

		for point in self.get_hitbox():
			if not self.map.is_point_on_road(point):
				return False
		return True

	def is_on_grass(self):
		if self.map is None:
			return True

		for point in self.get_hitbox():
			if self.map.is_point_on_road(point):
				return False
		return True
