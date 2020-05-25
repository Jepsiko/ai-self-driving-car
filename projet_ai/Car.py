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

		self.max_acceleration = 50
		self.max_steering = 40
		self.max_velocity = 160

		self.brake_deceleration = 90
		self.free_deceleration = 30

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
