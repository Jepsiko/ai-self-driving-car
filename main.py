import pygame
from Car import Car


if __name__ == "__main__":
	# Initialize pygame
	pygame.init()

	# Create the screen
	screen = pygame.display.set_mode((800, 600))

	# Title and Icon
	pygame.display.set_caption("Taxi Agent")
	icon = pygame.image.load("taxi.png")
	pygame.display.set_icon(icon)

	# Taxi taxi
	taxi = Car("car.png", 400, 300)

	# Level creation
	points = []

	# Game Loop
	running = True
	while running:
		for event in pygame.event.get():
			# If the red cross in the upper right corner is clicked
			if event.type == pygame.QUIT:
				running = False

		# Change the background color
		screen.fill((0, 50, 0))

		# Draw the taxi
		# taxi.draw(screen)

		# Level editing GUI
		pygame.draw.circle(screen, (150, 200, 150, 10), pygame.mouse.get_pos(), 10)
		for position in points:
			pygame.draw.circle(screen, (200, 200, 200, 10), position, 50)

		# Always update the display at the end of the loop
		pygame.display.update()
