import sys

import pygame
from ui_elements import PLAYERS_ICONS, set_images, draw_buttons, Hint, draw_list_buttons, ListButton, ButtonGroup
from save_data import current_data, Data
import items
import dialogue_system
from state import StateManager, State
from translatable_text import get_string
import pygame_gui
from input_manager import InputManager, MENU_LAYOUT
from main_movement import DungeonState
import settings
from game_resources import load_image
from music_manager import MusicManager


class MainMenu(State):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.input_layout = "ui"
        self.button_group = ButtonGroup(ListButton(get_string("new_game")),
                                        ListButton(get_string("load")),
                                        ListButton(get_string("language")),
                                        ListButton(get_string("quit")))

        background = pygame.sprite.Sprite()
        background.image = load_image("mainmenu_bg.png")
        MusicManager.play_music("mainmenu_theme.mp3", True)
        background.rect = background.image.get_rect()
        self.group = pygame.sprite.Group(background)
        InputManager.change_layout(self.input_layout)
        self.screen = Data.get_screen_size()

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if InputManager.current_key in InputManager.current_input:
                match InputManager.current_input[InputManager.current_key]:
                    case "Confirm":
                        if self.button_group.cur_index == 0:
                            StateManager.change_state(DungeonState())
                        elif self.button_group.cur_index == 1:
                            StateManager.change_state(DungeonState())
                        elif self.button_group.cur_index == 2:
                            StateManager.change_state(DungeonState())
                        elif self.button_group.cur_index == 3:
                            sys.exit()
                    case "Up":
                        self.button_group.prev_button()
                    case "Down":
                        self.button_group.next_button()

    def draw(self, screen: pygame.Surface):
        self.group.draw(screen)
        screen.blit(draw_buttons(Hint("navigation", "W", "S"),
                                 Hint("select", "Space")))
        draw_list_buttons(self.button_group, screen, 64, 64)


class Game:
    def __init__(self):
        pygame.init()
        self.is_fullscreen = True
        current_data.player_group.append(items.CHARACTERS["Samurai"])
        current_data.player_group.append(items.CHARACTERS["Kunoichi"])
        current_data.player_group.append(items.CHARACTERS["Archer"])
        current_data.player_group.append(items.CHARACTERS["Wizard"])
        current_data.set_leader(items.CHARACTERS["Samurai"])
        current_data.add_item(items.ITEMS["Aid"])
        current_data.add_item(items.ITEMS["Aid"])
        current_data.add_item(items.ITEMS["Aid_kit"])
        current_data.add_item(items.ITEMS["Imba"])
        set_images(current_data.player_group)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.screen = pygame.display.set_mode((700, 300))
        current_data.set_screen_size(self.screen.size)
        settings.set_wh(*Data.get_screen_size())

        self.clock = pygame.time.Clock()
        StateManager.change_state(MainMenu(self.screen))
        self.game()

    def game(self):

        running = True

        while running:
            time_delta = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    InputManager.listen(event.key)
                    if event.key == pygame.K_F11:

                        self.is_fullscreen = not self.is_fullscreen
                        if self.is_fullscreen:
                            self.screen = pygame.display.set_mode((700, 500))
                            current_data.set_screen_size(self.screen.size)
                        else:
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            current_data.set_screen_size(self.screen.size)
                StateManager.update(event)

            # self.battle_system.render_scene(self.screen)
            # self.screen.blit(dialogue_system.show_dialogue(get_string("dialogue_ex"), get_string("dummy")), (0, 0))
            StateManager.draw(self.screen)
            InputManager.reset_key()

            pygame.display.flip()


if __name__ == "__main__":
    difficults = {
        "peaceful": ("Безмятежный", 0, 0),
        "easy": ("Легкий", 0, 0),
        "normal": ("Стандартный", 0, 0),
        "hard": ("Сложный", 0, 0),
        "extreme": ("Смертельный", 0, 0),
    }
    game = Game()
