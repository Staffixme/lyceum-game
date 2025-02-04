import pygame.display

from state import StateManager, State

import items
from PIL import Image, ImageFilter, ImageEnhance
from music_manager import MusicManager
from random import randrange, choice

player_status = 'walk'


def attack_enemy():
    StateManager.change_state(DungeonToBattleState())


class DungeonToBattleState(State):
    def __init__(self):
        super().__init__()
        enemy_list = ["Magma", "Slime"]
        self.enemy_party = list()
        for i in range(randrange(1, 5)):
            self.enemy_party.append(items.create_enemy(choice(enemy_list)))
        self.is_ready_to_fight = False
        self.screenshot = pygame.display.get_surface()
        self.group = pygame.sprite.Group()
        MusicManager.play_music("battle_start.mp3")
        self.step = 0

        self.current_time = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 15

    def draw(self, screen):
        self.current_time = pygame.time.get_ticks()
        img = Image.frombytes("RGB", self.screenshot.size, pygame.image.tobytes(self.screenshot,"RGB"))
        if self.step < 5:
            self.group.empty()
            img = img.filter(ImageFilter.GaussianBlur(self.step))
            img = ImageEnhance.Brightness(img).enhance(1.3)

            img = img.tobytes()
            img = pygame.image.frombytes(img, self.screenshot.get_size(), "RGB")
            screen.blit(img, (0, 0))
        elif self.step > 25:
            from battle import BattleState
            StateManager.change_state(BattleState(self.enemy_party))

        if self.current_time - self.last_update > self.frame_delay:
            self.step += 1
            self.last_update = self.current_time




