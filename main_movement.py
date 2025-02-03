import pygame
from settings import *
from player import Player
import math
from map import world_map
from drawing import Drawing
from state import State
from ui_elements import draw_portraits
from save_data import current_data


class DungeonState(State):
    def __init__(self, screen):
        super().__init__()
        # sc = pygame.display.set_mode((WIDTH, HEIGHT))
        sc_map = pygame.Surface((screen[0] // MAP_SCALE, screen[1] // MAP_SCALE))
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.drawing = Drawing(sc_map)
        self.player_party = current_data.player_group

    def draw(self, screen):
        self.player.movement()
        screen.fill(BLACK)

        self.drawing.background(screen, self.player.angle)
        self.drawing.world(screen, self.player.pos, self.player.angle)
        self.drawing.mini_map(screen, self.player)
        screen.blit(draw_portraits(self.player_party), (0, 0))
