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

		self.speed = Vector2(0.1, 0.12)
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
		if isinstance(event, Event.TickEvent):
			delta = pygame.time.Clock().get_time() / 1000
			self.velocity += (self.acceleration * delta, 0)
			self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

			if self.steering:
				turn_rad = self.length / math.sin(math.radians(self.steering))
				velocity_angle = self.velocity.x / turn_rad
			else:
				velocity_angle = 0

			self.position += self.velocity.rotate(-self.angle) * delta
			self.angle += math.degrees(velocity_angle) * delta

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
