import sys

import pygame
from ui_elements import PLAYERS_ICONS, set_images, draw_buttons, Hint
from battle import BattleState
from save_data import current_data, Data
import items
import dialogue_system
from state import StateManager, State
from translatable_text import get_string
import pygame_gui
from input_manager import InputManager, MENU_LAYOUT
from main_movement import DungeonState
import settings


class MainMenu(State):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.input_layout = "menu"
        InputManager.change_layout(self.input_layout)
        self.screen = Data.get_screen_size()
        self.manager = pygame_gui.UIManager((self.screen[0], self.screen[1]), "data/ui styles/main_menu.json")

        self.new_game_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (375, 64)),
                                                         text=get_string("new_game"),
                                                         manager=self.manager)
        self.load_game_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 88), (375, 64)),
                                                          text=get_string("load"),
                                                          manager=self.manager)
        self.settings_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 176), (375, 64)),
                                                         text=get_string("settings"),
                                                         manager=self.manager)
        self.quit_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 264), (375, 64)),
                                                     text=get_string("quit"),
                                                     manager=self.manager)

    def update(self, event):
        self.manager.process_events(event)
        self.manager.update(60)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            match event.ui_element:
                case self.new_game_btn:
                    StateManager.change_state(DungeonState(self.screen))
                case self.quit_btn:
                    sys.exit()

    def draw(self, screen: pygame.Surface):
        screen.fill("blue")
        screen.blit(draw_buttons(Hint(get_string("navigation"), "W", "S"),
                    Hint(get_string("navigation"), "Space")))
        self.manager.draw_ui(screen)


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
        #self.screen = pygame.display.set_mode((700, 300))
        current_data.set_screen_size(self.screen.size)
        settings.set_wh(*Data.get_screen_size())
        print(settings.WIDTH)

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
