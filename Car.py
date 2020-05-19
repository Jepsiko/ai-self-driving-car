import pygame
from Lidar import Lidar
from math import sin, radians, degrees, copysign
from tools import *


class Car:

	def __init__(self, img, x, y):
		self.image = pygame.image.load(img)
		self.width = self.image.get_rect().height
		self.length = self.image.get_rect().width

		self.position = Vector2(x, y)
		self.lidar = Lidar(7, 6)

		self.speed = Vector2(0.1, 0.12)
		self.direction = Vector2(0, 0)

		self.angle = 0
		self.acceleration = 0
		self.steering = 0
		self.velocity = Vector2(0,0)

		self.max_acceleration = 5
		self.max_steering = 30
		self.max_velocity = 20
		
		self.brake_deceleration = 10
		self.free_deceleration = 2

	def update(self, screen, delta):
		#self.angle -= 0.1
		"""
		self.velocity += (self.acceleration * delta,0)
		self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

		if self.steering:
			turn_rad = self.length / sin(radians(self.steering))
			velocity_angle = self.velocity.x / turn_rad
		else :
			velocity_angle = 0
		
		self.position += self.velocity.rotate(-self.angle) * delta
		self.angle += degrees(velocity_angle) * delta
		"""
		self.position.x += self.speed.x * delta * self.direction.x
		self.position.y += self.speed.y * delta * self.direction.y
		#self.image.get_rect().topleft = self.position
		self.lidar.update(screen, self.position, -math.radians(self.angle))
	
	def from_angle(self, angle):
		# import math
		rads = math.radians(angle)
		self.direction = pygame.Vector2(math.sin(rads), math.cos(rads))
		
	
	def from_vector(self, vector):
		self.direction = (vector - self.position).normalize()

	def getState():
		return state

	def step():
		return step
	

	

