import random

import pygame
import pygame_gui

from save_data import Data, current_data
from ui_elements import (PLAYERS_ICONS, show_enemy_name, draw_portraits, draw_battle_ui, BattleButton, Icon,
                         ButtonGroup, ItemButton, draw_hp, draw_mp, draw_shield, draw_buttons, Hint)
from game_resources import BACKGROUNDS, load_image, load_font
from music_manager import MusicManager

import items
from state import State, StateManager
from dialogue_system import show_dialogue
from translatable_text import get_string
from input_manager import InputManager
from main_movement import DungeonState

from PIL import Image, ImageFilter


class BattleState(State):
    def __init__(self, enemy_group):
        super().__init__()
        self.is_win = False
        self.input_layout = "battle"
        InputManager.change_layout(self.input_layout)

        self.is_animation_play = False
        self.move_index = 0
        self.selected_enemy_index = 0
        self.selected_hero_index = 0

        self.player_party = current_data.player_group
        self.hero_count = len(self.player_party)
        self.enemy_party = enemy_group

        self.move_order = self.player_party + self.enemy_party

        self.screen = Data.get_screen_size()

        self.current_ui = "buttons"
        self.skill_group = ButtonGroup()
        self.items_group = ButtonGroup()

        self.target_type = None

        self.battle_buttons = (
            BattleButton(self.attack, Icon("attack_icon.png", (94, 94)), get_string("attack")),
            BattleButton(self.open_skills, Icon("skill_icon.png", (94, 94)), get_string("skill")),
            BattleButton(self.open_items, Icon("item_icon.png", (94, 94)), get_string("item")),
            BattleButton(self.defense, Icon("defense_icon.png", (94, 94)), get_string("defense")),
            BattleButton(self.escape, Icon("escape_icon.png", (94, 94)), get_string("escape"))
        )
        self.battle_icons = pygame.sprite.Group()
        self.button_group = ButtonGroup(*self.battle_buttons)

        for i in self.button_group.buttons:
            self.battle_icons.add(i.icon)

        self.enter()

    def enter(self):
        MusicManager.play_music(
            "battle_music.mp3", True)

        self.group = pygame.sprite.Group()

        self.player_point = pygame.sprite.Sprite(self.group)
        self.player_point.image = load_image("player_point.png")
        self.player_point.rect = self.player_point.image.get_rect()

        start_x = Data.get_screen_size()[0] // 4
        start_y = Data.get_screen_size()[1] // 4
        distance = 92
        for i in range(len(self.player_party)):
            self.group.add(self.player_party[i].sprites)
            self.player_party[i].sprites.change_animation("idle")
            self.player_party[i].sprites.rect.move_ip(start_x + i * distance, start_y + i * distance)

        start_x = 912
        start_y = 128
        for i in range(len(self.enemy_party)):
            self.group.add(self.enemy_party[i].sprites)
            self.enemy_party[i].sprites.rect.move_ip(start_x + i * distance, start_y + i * distance)

        self.crosschair = pygame.sprite.Sprite(self.group)
        self.crosschair.image = load_image("crosschair.png")
        self.crosschair.rect = self.crosschair.image.get_rect()
        self.crosschair_mode = "enemy"

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if InputManager.current_key in InputManager.current_input:
                match InputManager.current_input[InputManager.current_key]:
                    case "Select":
                        if self.target_type is None:
                            self.button_group.cur_button.press()
                        else:
                            if self.crosschair_mode == "enemy":
                                argument = self.enemy_party[self.selected_enemy_index]
                            else:
                                argument = self.player_party[self.selected_hero_index]
                            if self.target_type == "skills":
                                if self.player_party[self.move_index].cur_mana >= self.skill_group.cur_button.item.mp:
                                    if self.skill_group.cur_button.item.is_group_use:
                                        self.skill_group.cur_button.confirm((self.player_party, self.enemy_party))
                                    else:
                                        self.skill_group.cur_button.confirm(argument)
                                    self.player_party[self.move_index].cur_mana -= self.skill_group.cur_button.item.mp
                                    self.set_animation("skill")
                                    self.move()
                            elif self.target_type == "items":
                                if self.items_group.cur_button.item.is_group_use:
                                    self.items_group.cur_button.confirm((self.player_party, self.enemy_party))
                                else:
                                    self.items_group.cur_button.confirm(argument)
                                self.set_animation("item")
                                self.move()
                            self.target_type = None
                            self.crosschair_mode = "enemy"
                            self.current_ui = "buttons"
                    case "Next":
                        if self.crosschair_mode == "enemy":
                            self.selected_enemy_index = (self.selected_enemy_index + 1) % len(self.enemy_party)
                            if not self.enemy_party[self.selected_enemy_index].is_alive:
                                while not self.enemy_party[self.selected_enemy_index].is_alive:
                                    self.selected_enemy_index = (self.selected_enemy_index + 1) % len(self.enemy_party)
                        else:
                            self.selected_hero_index = (self.selected_hero_index + 1) % len(self.player_party)
                            if not self.player_party[self.selected_hero_index].is_alive:
                                while not self.player_party[self.selected_hero_index].is_alive:
                                    self.selected_hero_index = (self.selected_hero_index + 1) % len(self.player_party)
                    case "Prev":
                        if self.crosschair_mode == "enemy":
                            self.selected_enemy_index = (self.selected_enemy_index - 1) % len(self.enemy_party)
                            if not self.enemy_party[self.selected_enemy_index].is_alive:
                                while not self.enemy_party[self.selected_enemy_index].is_alive:
                                    self.selected_enemy_index = (self.selected_enemy_index - 1) % len(self.enemy_party)
                        else:
                            self.selected_hero_index = (self.selected_hero_index - 1) % len(self.player_party)
                            if not self.player_party[self.selected_hero_index].is_alive:
                                while not self.player_party[self.selected_hero_index].is_alive:
                                    self.selected_hero_index = (self.selected_hero_index - 1) % len(self.player_party)
                    case "Left":
                        self.button_group.prev_button()
                    case "Right":
                        self.button_group.next_button()
                    case "Back":
                        self.current_ui = "buttons"
                        self.input_layout = "battle"
                        InputManager.change_layout(self.input_layout)
                        self.target_type = None
                        self.crosschair_mode = "enemy"
                    case "Up":
                        if self.current_ui == "skills":
                            self.skill_group.prev_button()
                        else:
                            self.items_group.prev_button()
                    case "Down":
                        if self.current_ui == "skills":
                            self.skill_group.next_button()
                        else:
                            self.items_group.next_button()
                    case "Confirm":
                        if self.target_type is None:
                            if self.current_ui == "skills":
                                self.target_type = "skills"
                                group = self.skill_group
                            elif self.current_ui == "items":
                                self.target_type = "items"
                                group = self.items_group
                            self.current_ui = "target"
                            self.input_layout = "battle"
                            InputManager.change_layout(self.input_layout)
                            item = group.cur_button.item
                            if isinstance(item, items.HealItem) or isinstance(item, items.HealSkill):
                                self.crosschair_mode = "hero"
                            else:
                                self.crosschair_mode = "enemy"

    def set_animation(self, name):
        self.move_order[self.move_index].sprites.change_animation(name)

    def play_animations(self):
        for i in self.player_party:
            if i.is_alive or (i.sprites.animation_index + 1 != len(i.sprites.defeated_state)
                              and i.sprites.animation == "defeated"):
                i.sprites.draw()
        for i in self.enemy_party:
            if i.is_alive or (i.sprites.animation_index + 1 != len(i.sprites.defeated_state)
                              and i.sprites.animation == "defeated"):
                i.sprites.draw()

    def check_animation(self):
        if list(filter(lambda x: x.sprites.is_play, self.move_order)):
            return True
        return False

    def attack(self):
        self.player_party[self.move_index].attack(self.enemy_party[self.selected_enemy_index])
        self.set_animation("attack")
        print("next move")
        self.move()

    def open_skills(self):
        skills = list()
        for i in self.player_party[self.move_index].skills:
            match type(i):
                case items.AttackSkill:
                    color = "#F87401"
                case items.HealSkill:
                    color = "#0DBE51"
            skills.append(ItemButton(i, i.name, i.description, color))
        self.skill_group.set_buttons(*skills)
        self.input_layout = "ui"
        InputManager.change_layout(self.input_layout)
        self.current_ui = "skills"

    def open_items(self):
        current_data.update_items()
        if current_data.get_items():
            item_list = list()
            for i in current_data.get_items():
                match type(i):
                    case items.AttackItem:
                        color = "#F87401"
                    case items.HealItem:
                        color = "#0DBE51"
                item_list.append(ItemButton(i, i.name, i.description, color))
            self.items_group.set_buttons(*item_list)
            self.input_layout = "ui"
            InputManager.change_layout(self.input_layout)
            self.current_ui = "items"

    def defense(self):
        self.player_party[self.move_index].is_protected = True
        self.player_party[self.move_index].sprites.change_animation("defense")
        self.move()

    def escape(self):
        random_result = random.randrange(1, 4)
        if random_result == 3:
            StateManager.change_state(BattleFinishState("escape"))
        else:
            self.move()

    def is_enemies_defeated(self):
        alive_count = 0
        for i in self.enemy_party:
            if not i.is_alive:
                alive_count += 1
        if alive_count == len(self.enemy_party):
            self.is_win = True
            return True
        return False

    def move(self):
        if not self.is_enemies_defeated():
            self.move_index = (self.move_index + 1) % len(self.move_order)
            if isinstance(self.move_order[self.move_index], items.Enemy):
                self.is_player_move = False
                while isinstance(self.move_order[self.move_index], items.Enemy):
                    if self.move_order[self.move_index].is_alive:
                        character = random.choice(self.player_party)
                        while not character.is_alive:
                            character = random.choice(self.player_party)
                        self.set_animation("attack")
                        self.move_order[self.move_index].attack(character)

                        if not character.is_alive:
                            self.move_order.remove(character)
                        if character.is_leader and not character.is_alive:
                            StateManager.change_state(GameOverState())
                            break

                    self.move_index = (self.move_index + 1) % len(self.move_order)

                for i in list(filter(lambda x: isinstance(x, items.Hero), self.move_order)):
                    i.is_protected = False

            if not self.enemy_party[self.selected_enemy_index].is_alive:
                while not self.enemy_party[self.selected_enemy_index].is_alive:
                    self.selected_enemy_index = (self.selected_enemy_index + 1) % len(self.enemy_party)

    def draw(self, screen: pygame.Surface):
        surface = pygame.Surface(Data.screen_size)
        BACKGROUNDS.draw(surface)
        if isinstance(self.move_order[self.move_index], items.Hero):
            self.player_point.rect = self.move_order[self.move_index].sprites.rect
            self.player_point.rect = self.player_point.rect.move(0, 128)

        if self.crosschair_mode == "enemy":
            self.crosschair.rect = self.enemy_party[self.selected_enemy_index].sprites.rect
            self.crosschair.rect = self.crosschair.rect.move(92, 92)
        else:
            self.crosschair.rect = self.player_party[self.selected_hero_index].sprites.rect
            self.crosschair.rect = self.crosschair.rect.move(92, 92)

        self.group.draw(surface)
        self.play_animations()

        screen.blit(surface, (0, 0))
        screen.blit(show_enemy_name(self.enemy_party[self.selected_enemy_index].name), (0, 0))
        screen.blit(draw_portraits(self.player_party), (0, 0))

        for i in self.player_party:
            if i.is_protected and i.is_alive:
                draw_shield(i.sprites.rect.x + 112, i.sprites.rect.y + 28, screen)

        if not self.check_animation():
            if self.crosschair_mode == "enemy":
                draw_hp(self.enemy_party[self.selected_enemy_index], self.crosschair.rect.x + 64,
                        self.crosschair.rect.y - 16, screen)
            else:
                draw_hp(self.player_party[self.selected_hero_index], self.crosschair.rect.x + 64,
                        self.crosschair.rect.y - 42, screen)
                draw_mp(self.player_party[self.selected_hero_index], self.crosschair.rect.x + 64,
                        self.crosschair.rect.y - 16, screen)

            screen.blit(draw_battle_ui(self.current_ui, self.button_group, self.battle_icons, self.skill_group,
                                       self.items_group)[0], (0, 0))
            screen.blit(draw_battle_ui(self.current_ui, self.button_group, self.battle_icons, self.skill_group,
                                       self.items_group)[1], (0, 0))
        if self.is_win:
            current_screen = pygame.image.tobytes(screen, "RGB")
            background = Image.frombytes("RGB", Data.get_screen_size(), current_screen)
            background = background.filter(ImageFilter.GaussianBlur(24))
            background = background.tobytes()
            background = pygame.image.frombytes(background, Data.get_screen_size(), "RGB")
            start_x = Data.get_screen_size()[0] // 4
            start_y = Data.get_screen_size()[1] // 4
            distance = 92
            for i in range(len(self.player_party)):
                self.player_party[i].sprites.rect.move_ip(-start_x - i * distance, -start_y - i * distance)
                if not self.player_party[i].is_alive:
                    self.player_party[i].heal(1)
                    self.player_party[i].is_alive = True
            StateManager.change_state(BattleFinishState("win", background))

        # screen.blit(show_dialogue(get_string("dialogue_ex"), get_string("dummy")))


class BattleFinishState(State):
    def __init__(self, end_type: str, background=None):
        super().__init__()
        InputManager.change_layout("ui")
        MusicManager.play_music("battle_end_music.mp3", True)
        if end_type == "win":
            self.title = "ПОБЕДА!"
            self.fill_mode = "image"
            sprite = pygame.sprite.Sprite()
            sprite.image = background
            sprite.rect = sprite.image.get_rect()
            self.group = pygame.sprite.Group(sprite)
        else:
            self.title = "ПОБЕГ"
            self.fill_mode = "color"

        self.hero = pygame.sprite.Sprite()
        self.frames = self.cut_sheet(load_image("Run.png"), 8)
        self.hero.image = self.frames[0]
        self.hero.rect = self.hero.image.get_rect()
        self.hero_group = pygame.sprite.Group(self.hero)
        # self.hero.rect.move_ip(0, 500)
        self.hero_animation_index = 0

        self.current_time = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 90

    def cut_sheet(self, sprite, count):
        frames = list()
        self.hero.rect = pygame.Rect(0, 0, sprite.get_width() // count, sprite.get_height())
        for i in range(count):
            frame_location = (self.hero.rect.w * i, 0)
            frame = sprite.subsurface(pygame.Rect(frame_location, self.hero.rect.size))
            frame = pygame.transform.scale(frame, (512, 512))
            frames.append(frame)

        return frames

    def update(self, event):
        if event.type == pygame.KEYDOWN:
            if InputManager.current_key in InputManager.current_input:
                match InputManager.current_input[InputManager.current_key]:
                    case "Confirm":
                        StateManager.change_state(DungeonState())

    def run_animation(self, screen):
        self.current_time = pygame.time.get_ticks()
        if self.current_time - self.last_update > self.frame_delay:
            self.hero_animation_index = (self.hero_animation_index + 1) % len(self.frames)
            self.last_update = self.current_time
            if self.hero.rect.x < 256:
                self.hero.rect.move_ip(10, 0)

        self.hero.image = self.frames[self.hero_animation_index]

        self.hero_group.draw(screen)

    def draw(self, screen):
        if self.fill_mode == "image":
            self.group.draw(screen)
        else:
            screen.fill("gray")
        win_text = pygame.font.Font(load_font("Unbounded-Black.ttf"), 128)
        screen.blit(
            win_text.render(self.title, True, "white"),
            (Data.get_screen_size()[0] - win_text.size(self.title)[0] - 90,
             Data.get_screen_size()[1] / 2 - win_text.size(self.title)[1] - 64))
        self.run_animation(screen)
        screen.blit(draw_buttons(Hint("continue", "Space")), (0, 0))


class GameOverState(State):
    def __init__(self):
        super().__init__()
        MusicManager.stop_music()

    def draw(self, screen):
        screen.fill("black")
        win_text = pygame.font.Font(None, 62)
        screen.blit(
            win_text.render("Игра окончена", True, "white"),
            (Data.screen_size[0] / 2 - win_text.size("Игра окончена")[0],
             Data.screen_size[1] / 2 - win_text.size("Игра окончена")[1]))
