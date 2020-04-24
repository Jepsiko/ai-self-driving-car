import pygame

if __name__ == "__main__":
	# Initialize pygame
	pygame.init()

	# Create the screen
	screen = pygame.display.set_mode((800, 640))

	# Title and Icon
	pygame.display.set_caption("Taxi Agent")
	icon = pygame.image.load("taxi.png")
	pygame.display.set_icon(icon)

	# Game Loop
	running = True
	while running:
		for event in pygame.event.get():
			# If the red cross in the upper right corner is clicked
			if event.type == pygame.QUIT:
				running = False

		# Change the background color
		screen.fill((0, 50, 0))

		# Always update the display at the end of the loop
		pygame.display.update()
