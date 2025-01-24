import random

import pygame
import pygame_gui

from save_data import Data, current_data
from ui_elements import (PLAYERS_ICONS, show_enemy_name, draw_portraits, draw_battle_ui, BattleButton, Icon,
                         ButtonGroup, ItemButton, draw_hp, draw_mp)
from game_resources import BACKGROUNDS, load_image, load_font
from music_manager import MusicManager

import items
from state import State, StateManager
from dialogue_system import show_dialogue
from translatable_text import get_string
from input_manager import InputManager


class BattleState(State):
    def __init__(self, enemy_group):
        super().__init__()
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

        start_x = 425
        start_y = 375
        distance = 92
        for i in range(len(self.player_party)):
            self.group.add(self.player_party[i].sprites)
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
                                    self.move()
                            elif self.target_type == "items":
                                if self.items_group.cur_button.item.is_group_use:
                                    self.items_group.cur_button.confirm((self.player_party, self.enemy_party))
                                else:
                                    self.items_group.cur_button.confirm(argument)
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
                            if (isinstance(item, items.HealItem) or isinstance(item, items.HealSkill)
                                    or isinstance(item, items.BorrowingSkill)):
                                self.crosschair_mode = "hero"
                            else:
                                self.crosschair_mode = "enemy"

    def set_animation(self, name):
        self.move_order[self.move_index].sprites.change_animation(name)

    def play_animations(self):
        for i in self.move_order:
            i.sprites.draw()

    def check_animation(self):
        if filter(lambda x: x.sprites.is_play, self.move_order):
            return False
        return True

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
                case items.AbsorbingSkill:
                    color = "#51436C"
                case items.BorrowingSkill:
                    color = "#43666C"
                case items.SpecialSkill:
                    color = "#FF517C"
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
                    case items.AttackSkill:
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
            StateManager.change_state(BattleFinishState("win"))
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
                        while self.move_order[self.move_index].sprites.animation != "idle":
                            self.play_animations()
                        self.move_order[self.move_index].attack(character)

                        if not character.is_alive:
                            self.move_order.remove(character)
                        if character.is_leader and not character.is_alive:
                            StateManager.change_state(GameOverState())
                            break

                    self.move_index = (self.move_index + 1) % len(self.move_order)

                for i in filter(lambda x: isinstance(x, items.Hero), self.move_order):
                    i.is_protected = False
                    i.sprites.change_animation("idle")

            if not self.enemy_party[self.selected_enemy_index].is_alive:
                while not self.enemy_party[self.selected_enemy_index].is_alive:
                    self.selected_enemy_index = (self.selected_enemy_index + 1) % len(self.enemy_party)

    def draw(self, screen: pygame.Surface):
        surface = pygame.Surface(Data.screen_size)
        BACKGROUNDS.draw(surface)
        if isinstance(self.move_order[self.move_index], items.Hero):
            self.player_point.rect = self.move_order[self.move_index].sprites.rect
            self.player_point.rect = self.player_point.rect.move(0, 98)

        if self.crosschair_mode == "enemy":
            self.crosschair.rect = self.enemy_party[self.selected_enemy_index].sprites.rect
            self.crosschair.rect = self.crosschair.rect.move(92, 92)
        else:
            self.crosschair.rect = self.player_party[self.selected_hero_index].sprites.rect
            self.crosschair.rect = self.crosschair.rect.move(92, 92)

        self.group.draw(surface)
        # self.play_animations()

        screen.blit(surface, (0, 0))
        screen.blit(show_enemy_name(self.enemy_party[self.selected_enemy_index].name), (0, 0))
        screen.blit(draw_portraits(self.player_party), (0, 0))

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

        # screen.blit(show_dialogue(get_string("dialogue_ex"), get_string("dummy")))


class BattleFinishState(State):
    def __init__(self, end_type: str):
        super().__init__()
        MusicManager.play_music("battle_end_music.mp3", True)
        if end_type == "win":
            self.title = "Победа"
            self.color = "blue"
        else:
            self.title = "Побег"
            self.color = "gray"

    def draw(self, screen):
        screen.fill(self.color)
        win_text = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 62)
        screen.blit(
            win_text.render(self.title, True, "white"),
            (42, 42))


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
