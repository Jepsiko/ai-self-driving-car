import pygame

# Window
WIDTH = 1366
HEIGHT = 768

# Point editing
MIN_DIST_POINTS = 150

# Level Design
GRASS_COLOR = (0, 100, 0)
ROAD_COLOR = (80, 80, 80)
ROAD_WIDTH = 50
CAR_IMAGE = 'car.png'

# Level Editing
DIST_SELECT_POINT = 40
CROSSING_ROAD_COLOR = (150, 100, 100)

# Lidar View
LIDAR_VIEW_SQUARE_SIZE = 15
LIDAR_VIEW_BORDER_SIZE = 5
LIDAR_VIEW_GRASS = (0, 150, 0)
LIDAR_VIEW_ROAD = (100, 100, 100)
LIDAR_VIEW_BORDER_COLOR = (0, 0, 0)

# Debug Design
DEBUG = False
CAR_HITBOX_COLOR = (0, 0, 200)
LIDAR_BOX_COLOR = (200, 0, 0)
LIDAR_POINTS_COLOR = (0, 255, 0)

# Keyboard Commands
KEY_QUIT = pygame.K_ESCAPE          # ESC
KEY_POINT_EDITING = pygame.K_p      # P
KEY_LINE_EDITING = pygame.K_l       # L
KEY_PLAY_MODE = pygame.K_f          # F
KEY_TOGGLE_DEBUG = pygame.K_d       # D
KEY_MOVE_FRONT = pygame.K_UP        # UP
KEY_MOVE_BACK = pygame.K_DOWN       # DOWN
KEY_MOVE_LEFT = pygame.K_LEFT       # LEFT
KEY_MOVE_RIGHT = pygame.K_RIGHT     # RIGHT

# Mouse Commands
MOUSE_CREATE = 1                    # LEFT CLIC
MOUSE_REMOVE = 3                    # RIGHT CLIC
