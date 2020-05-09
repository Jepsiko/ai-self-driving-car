import pygame
from pygame.math import Vector2

class Sensor:

    def __init__(self, start, length):#4,8,16,32,64,....
        self.start = start
        #print("pos", start)
        self.end = Vector2(start[0]+length, start[1])



    def sensor_draw(screen):
        pygame.draw.line(screen,(200, 0, 0 ), pos, position2,2)
"""
    def get_distance(self, sensor):
        pos = Car.get_pos(taxi)
        
        position2 = Vector2(pos[0] + 200, pos[1])
"""
