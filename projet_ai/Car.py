import pygame
from projet_ai.Lidar import Lidar
from pygame import Vector2
import math
from projet_ai import Event


class Car(Event.Listener):

	def __init__(self, img, evManager):
		super().__init__(evManager)
		self.image = pygame.image.load(img)
		self.width = self.image.get_rect().height
		self.length = self.image.get_rect().width

		self.position = Vector2(0, 0)
		self.lidar = Lidar(7, 6)

		self.direction = Vector2(0, 0)

		self.angle = 0
		self.acceleration = 0
		self.steering = 0
		self.velocity = Vector2(0, 0)

		self.max_acceleration = 5
		self.max_steering = 30
		self.max_velocity = 20

		self.brake_deceleration = 10
		self.free_deceleration = 2

	def notify(self, event):
		if isinstance(event, Event.MovePlayerEvent):
			direction = event.direction
			delta = 0.1

			if direction.x == 1:
				if self.velocity.x < 0:
					self.acceleration = self.brake_deceleration
				else:
					self.acceleration += 1 * delta
			elif direction.x == -1:
				if self.velocity.x > 0:
					self.acceleration = -self.brake_deceleration
				else:
					self.acceleration -= 1 * delta
			else:
				if abs(self.velocity.x) > delta * self.free_deceleration:
					self.acceleration = -math.copysign(self.free_deceleration, self.velocity.x)
				else:
					if delta != 0:
						self.acceleration = -self.velocity.x / delta
			self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))

			if direction.y == 1:
				self.steering -= 30 * delta
			elif direction.y == -1:
				self.steering += 30 * delta
			else:
				self.steering = 0
			self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

			self.evManager.post(Event.CarUpdatedEvent(self))

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
