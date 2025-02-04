import pygame
from settings import *
from player import Player
import math
from map import world_map
from drawing import Drawing
from state import State
from ui_elements import draw_portraits, draw_buttons, Hint
from save_data import current_data
from translatable_text import get_string
from music_manager import MusicManager


class DungeonState(State):
    def __init__(self):
        super().__init__()
        # sc = pygame.display.set_mode((WIDTH, HEIGHT))
        MusicManager.play_music("schooldays.mp3", True)
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.drawing = Drawing()
        self.player_party = current_data.player_group

    def draw(self, screen):
        self.player.movement()
        screen.fill(BLACK)

        self.drawing.background(screen, self.player.angle)
        self.drawing.world(screen, self.player.pos, self.player.angle)
        screen.blit(self.drawing.mini_map(self.player), (32, 52))
        screen.blit(draw_portraits(self.player_party), (0, 0))
        screen.blit(draw_buttons(Hint("menu", "Tab"), Hint("save", "H")), (0, 0))
