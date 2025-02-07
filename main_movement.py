import pygame
from settings import *
from player import Player
import math
from map import world_map
from drawing import Drawing
from state import State, StateManager
from ui_elements import draw_portraits, draw_buttons, Hint, ListButton, draw_list_buttons, draw_blue_rect, ButtonGroup, \
    print_stage, draw_item_info_rect, GameSaveButton, draw_save_buttons
import save_data
from translatable_text import get_string
from music_manager import MusicManager
from input_manager import InputManager
from PIL import Image, ImageFilter


class DungeonState(State):
    def __init__(self):
        super().__init__()
        InputManager.change_layout("movement")
        self.mode = "gameplay"

        self.group = pygame.sprite.Group()
        MusicManager.play_music("dungeon_theme.mp3", True)
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.drawing = Drawing()
        self.player_party = save_data.current_data.player_group

        self.save_buttons_group = ButtonGroup(GameSaveButton(f"{get_string("save")} №1", save_data.Data.load_stage(1)),
                                              GameSaveButton(f"{get_string("save")} №2", save_data.Data.load_stage(2)),
                                              GameSaveButton(f"{get_string("save")} №3", save_data.Data.load_stage(3)))

        self.menu_buttons = ButtonGroup(ListButton(get_string("use_item")),
                                        ListButton(get_string("load")), ListButton(get_string("to_menu")))
        self.items_buttons = ButtonGroup()
        self.selected_character_index = 0

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if InputManager.current_key in InputManager.current_input:
                match InputManager.current_input[InputManager.current_key]:
                    case "Save":
                        self.get_blurred_background()
                        InputManager.change_layout("ui")
                        self.mode = "save"
                    case "Menu":
                        self.get_blurred_background()
                        InputManager.change_layout("ui")
                        self.mode = "menu"
                    case "Back":
                        if self.mode == "menu" or self.mode == "save":
                            InputManager.change_layout("movement")
                            self.ui_background = None
                            self.mode = "gameplay"
                        elif self.mode == "items":
                            self.mode = "menu"
                        elif self.mode == "load":
                            self.mode = "menu"
                    case "Up":
                        if self.mode == "menu":
                            self.menu_buttons.prev_button()
                        elif self.mode == "items":
                            self.items_buttons.prev_button()
                        elif self.mode == "save":
                            self.save_buttons_group.prev_button()
                        elif self.mode == "load":
                            self.save_buttons_group.prev_button()
                    case "Down":
                        if self.mode == "menu":
                            self.menu_buttons.next_button()
                        elif self.mode == "items":
                            self.items_buttons.next_button()
                        elif self.mode == "save":
                            self.save_buttons_group.next_button()
                        elif self.mode == "load":
                            self.save_buttons_group.next_button()
                    case "Confirm":
                        if self.mode == "menu":
                            if self.menu_buttons.cur_index == 0:
                                print(save_data.current_data.get_items())
                                if save_data.current_data.get_items():
                                    self.mode = "items"
                                    self.set_item_buttons()
                            elif self.menu_buttons.cur_index == 1:
                                self.mode = "load"
                            elif self.menu_buttons.cur_index == 2:
                                from main import MainMenu
                                StateManager.change_state(MainMenu(pygame.display.get_surface()))
                        elif self.mode == "save":
                            save_data.Data.save_game(self.save_buttons_group.cur_index + 1,
                                                     save_data.current_data.get_items(),
                                                        save_data.current_data.stage,
                                                     save_data.current_data.player_group)
                            self.save_buttons_group.cur_button.make_save(save_data.current_data.stage)
                        elif self.mode == "items":
                            (save_data.current_data.player_items[self.items_buttons.cur_index]
                             .use(save_data.current_data.player_group[self.selected_character_index]))
                            self.set_item_buttons()
                        elif self.mode == "load":
                            save_data.Data.load_game(self.save_buttons_group.cur_index + 1, save_data.current_data)
                            StateManager.change_state(DungeonState())
                    case "Left":
                        if self.mode == "items":
                            self.selected_character_index = ((self.selected_character_index - 1) %
                                                             len(save_data.current_data.player_group))
                    case "Right":
                        if self.mode == "items":
                            self.selected_character_index = ((self.selected_character_index + 1) %
                                                             len(save_data.current_data.player_group))

    def set_item_buttons(self):
        self.items_buttons.buttons.clear()
        buttons = list()
        for i in save_data.current_data.get_items():
            buttons.append(ListButton(f"{i.name} - {i.count}", 42))

        self.items_buttons.set_buttons(*buttons)

    def get_blurred_background(self):
        self.group.empty()
        screen = pygame.display.get_surface()
        current_screen = pygame.image.tobytes(screen, "RGB")
        background = Image.frombytes("RGB", save_data.Data.get_screen_size(), current_screen)
        background = background.filter(ImageFilter.GaussianBlur(64))
        background = background.tobytes()
        background = pygame.image.frombytes(background, save_data.Data.get_screen_size(), "RGB")

        ui_background = pygame.sprite.Sprite()
        ui_background.image = background
        ui_background.rect = ui_background.image.get_rect()
        self.group = pygame.sprite.Group(ui_background)

    def draw(self, screen):
        self.player.movement()
        screen.fill(BLACK)
        match self.mode:
            case "gameplay":
                self.drawing.background(screen, self.player.angle)
                self.drawing.world(screen, self.player.pos, self.player.angle)
                mini_map = self.drawing.mini_map(self.player)
                screen.blit(mini_map, (32, 52))
                screen.blit(print_stage(0), (32, mini_map.size[1] + 24))
                screen.blit(draw_portraits(self.player_party), (0, 0))
                screen.blit(draw_buttons(Hint("menu", "Tab"),
                                         Hint("save", "H")), (0, 0))
            case "menu":
                self.group.draw(screen)
                draw_list_buttons(self.menu_buttons, screen, 90, 90)
                draw_blue_rect(screen)
                screen.blit(draw_portraits(self.player_party), (0, 0))
                screen.blit(draw_buttons(Hint("back", "Esc"),
                                         Hint("select", "Space")), (0, 0))
            case "save":
                self.group.draw(screen)
                draw_save_buttons(self.save_buttons_group, screen, screen.size[0] // 2 - 464, screen.size[1] // 5)
                screen.blit(draw_buttons(Hint("back", "Esc"),
                                         Hint("navigation", "W", "S"),
                                         Hint("save", "Space")), (0, 0))
            case "load":
                self.group.draw(screen)
                draw_save_buttons(self.save_buttons_group, screen, screen.size[0] // 2 - 464, screen.size[1] // 5)
                screen.blit(draw_buttons(Hint("back", "Esc"),
                                         Hint("navigation", "W", "S"),
                                         Hint("load", "Space")), (0, 0))
            case "items":
                self.group.draw(screen)
                draw_list_buttons(self.items_buttons, screen, 90, 90, 72)
                draw_item_info_rect(screen, save_data.current_data.player_items[self.items_buttons.cur_index].name,
                                    save_data.current_data.player_items[self.items_buttons.cur_index].description,
                                    save_data.current_data.player_items[self.items_buttons.cur_index].count,
                                    save_data.current_data.player_group[self.selected_character_index].name)
                screen.blit(draw_portraits(self.player_party), (0, 0))
                screen.blit(draw_buttons(Hint("back", "Esc"),
                                         Hint("navigation", "W", "S"),
                                         Hint("target_selection", "A", "D"),
                                         Hint("select", "Space")), (0, 0))
