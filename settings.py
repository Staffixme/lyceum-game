import math

# game settings
WIDTH = 0
HEIGHT = 0
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
TILE = 100
FPS_POS = (WIDTH - 65, 5)

# minimap settings
MAP_SCALE = 6
MAP_TILE = TILE // MAP_SCALE
MAP_POS = (0, HEIGHT - HEIGHT // MAP_SCALE)

# ray casting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 400
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE
SCALE = WIDTH // NUM_RAYS

# texture settings (1200 x 1200)
TEXTURE_WIDTH = 1200
TEXTURE_HEIGHT = 1200
TEXTURE_SCALE = TEXTURE_WIDTH // TILE

# player settings
player_pos = (150, 150)
player_angle = 0

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 80, 0)
BLUE = (0, 0, 255)
DARKGRAY = (40, 40, 40)
PURPLE = (120, 0, 120)
SKYBLUE = (0, 186, 255)
YELLOW = (220, 220, 0)
SANDY = (244, 164, 96)


def set_wh(w, h):
    global WIDTH, HEIGHT, HALF_WIDTH, HALF_HEIGHT, SCALE, FOV, HALF_FOV, NUM_RAYS, MAX_DEPTH, DELTA_ANGLE, DIST, PROJ_COEFF
    WIDTH = w
    HEIGHT = h
    HALF_WIDTH = WIDTH // 2
    HALF_HEIGHT = HEIGHT // 2
    FOV = math.pi / 3
    HALF_FOV = FOV / 2
    NUM_RAYS = w // 8
    MAX_DEPTH = 800
    DELTA_ANGLE = FOV / NUM_RAYS
    DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
    PROJ_COEFF = 3 * DIST * TILE
    SCALE = WIDTH // NUM_RAYS
    SCALE = WIDTH // NUM_RAYS
