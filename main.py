import pygame

if __name__ == "__main__":
	# Initialize pygame
	pygame.init()

	# Create the screen
	screen = pygame.display.set_mode((800, 640))

	# Game Loop
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
