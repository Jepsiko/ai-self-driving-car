
def ccw(A, B, C):
	return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)


def is_line_crossing(line1, line2):
	A, B = line1
	C, D = line2

	# Prevent lines starting from the same point from being noticed as crossed lines
	if A == C or A == D or B == C or B == D:
		return False

	return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
