from pygame.math import Vector2
import math


def get_point_at_vector(pos, magnitude, angle):
	return Vector2(pos.x + magnitude * math.cos(angle), pos.y + magnitude * math.sin(angle))


def ccw(A, B, C):
	return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


def is_line_crossing(line1, line2):
	A, B = line1
	C, D = line2

	# Prevent lines starting from the same point from being noticed as crossed lines
	if A == C or A == D or B == C or B == D:
		return False

	return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
