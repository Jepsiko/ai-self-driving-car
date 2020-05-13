

class Agent:

	def __init__(self, lidar):
		self.input_size = lidar.row * lidar.col + 2
		self.output_size = 2
