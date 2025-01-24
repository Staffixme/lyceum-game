import pygame
import os
import sys
import math

from game_resources import load_image, load_font
from save_data import Data
from translatable_text import get_string
from input_manager import InputManager
from items import Skill, Item, AttackSkill
from game_resources import CHARACTERS_PORTRAITS, Icon, CharacterIcon

PLAYERS_ICONS = pygame.sprite.Group()


class Button:
    def __init__(self):
        self.is_active = False

    def set_active(self):
        pass

    def set_inactive(self):
        pass

    def press(self):
        pass


class ButtonGroup:
    def __init__(self, *buttons: Button | None):
        if buttons:
            self.buttons = list(buttons)
            self.cur_index = 0
            self.cur_button = self.buttons[self.cur_index]
            self.cur_button.set_active()

    def next_button(self):
        self.cur_button.set_inactive()
        self.cur_index = (self.cur_index + 1) % len(self.buttons)
        self.cur_button = self.buttons[self.cur_index]
        self.cur_button.set_active()

    def prev_button(self):
        self.cur_button.set_inactive()
        self.cur_index = (self.cur_index - 1) % len(self.buttons)
        self.cur_button = self.buttons[self.cur_index]
        self.cur_button.set_active()

    def set_buttons(self, *buttons: Button):
        self.buttons = list(buttons)
        self.cur_index = 0
        self.cur_button = self.buttons[self.cur_index]
        self.cur_button.set_active()


class ItemButton(Button):
    def __init__(self, item, name: str, description: str, color):
        super().__init__()
        self.text = name
        self.description = description
        self.active_color = color
        self.inactive_color = "#B5B5B5"
        self.active_text = "white"
        self.inactive_text = "black"
        self.current_text = self.inactive_text
        self.current_color = self.inactive_color
        self.item = item

    def set_active(self):
        self.current_color = self.active_color
        self.current_text = self.active_text

    def set_inactive(self):
        self.current_color = self.inactive_color
        self.current_text = self.inactive_text

    def confirm(self, target):
        if isinstance(self.item, Skill):
            self.item.use_skill(target)
        elif isinstance(self.item, Item):
            self.item.use(target)


class Hint:
    def __init__(self, text: str, *key_unicode: str):
        self.key = key_unicode
        self.text = text

    def draw(self, x, y, surface):
        keys = "/".join(self.key)
        key = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 18)
        bg = pygame.draw.rect(surface, "#ECECEC", (x, y, key.size(keys)[0] + 24, 42), 0, 5)
        text = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 24)
        surface.blit(key.render(keys, True, "black"),
                     (bg.x + 12, bg.y + 10))
        surface.blit(text.render(get_string(self.text), True, "white"),
                     (bg.size[0] + 42, bg.y + 4))


class BattleButton(Button):
    def __init__(self, function, icon: Icon, text: str):
        super().__init__()
        self.function = function
        self.icon = icon
        self.text = text
        self.icon.image.convert_alpha()
        self.icon.image.set_alpha(100)

    def set_active(self):
        self.icon.image.set_alpha(255)

    def set_inactive(self):
        self.icon.image.set_alpha(100)

    def press(self):
        self.function()


def show_enemy_name(name):
    surface = pygame.surface.Surface((1920, 1080), pygame.SRCALPHA, 32)
    bubble = pygame.draw.rect(surface, "#EEEEEE", (surface.width - 324, 24, 300, 64), 0, 25)
    name_text = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 32)
    surface.blit(name_text.render(name, True, "black"), (bubble.x + 11, bubble.y + 11))
    return surface


def set_images(characters):
    for i in characters:
        PLAYERS_ICONS.add(i.portrait.icon)


def draw_portraits(characters):
    surface = pygame.surface.Surface(Data.get_screen_size(), pygame.SRCALPHA, 32)
    start_x = -200
    distance = 150

    for i in range(len(characters)):
        character = characters[i]

        character.portrait.icon.rect.x = surface.size[0]
        character.portrait.icon.rect.y = surface.size[1]
        character.portrait.icon.rect = character.portrait.icon.rect.move(start_x - i * distance, -275)
        character.portrait.draw_hp_bar(surface, surface.size[0] + (-166 - i * distance), surface.size[1] - 80,
                                       130, 15, character.cur_health, character.health)
        character.portrait.draw_mp_bar(surface, surface.size[0] + (-166 - i * distance), surface.size[1] - 30,
                                       130, 15, character.cur_mana, character.mana)

    PLAYERS_ICONS.draw(surface)

    return surface


def draw_battle_buttons(group, battle_icons):
    surface = pygame.surface.Surface(Data.get_screen_size(), pygame.SRCALPHA, 32)
    radius = 150
    center_x, center_y = 300, Data.get_screen_size()[1] - 350
    tooltip = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 28)
    surface.blit(tooltip.render(group.cur_button.text, True, "black"),
                 (group.cur_button.icon.rect.x + 52, group.cur_button.icon.rect.y + 92))

    for i in range(len(group.buttons)):
        button = group.buttons[i].icon
        angle = 2 * math.pi * i / len(group.buttons)
        button.rect.x = center_x + radius * math.cos(angle)
        button.rect.y = center_y + radius * math.sin(angle)
    battle_icons.draw(surface)

    return surface


def draw_skills(skill_group):
    surface = pygame.surface.Surface(Data.get_screen_size(), pygame.SRCALPHA, 32)
    screen_size = Data.get_screen_size()
    panel = pygame.draw.rect(surface, "#ECECEC", (42, screen_size[1] // 3, 440, 605), 0, 15)

    title = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 32)
    surface.blit(title.render(get_string("use_skill"), True, "black"),
                 (panel.x + 24, panel.y + 24))

    info = pygame.draw.rect(surface, "white", (panel.x + 24, panel.y + 76, 392, 87), 0, 5)
    name_text = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 20)
    surface.blit(name_text.render(skill_group.cur_button.text, True, "black"),
                 (info.x + 15, info.y + 15))
    description_text = pygame.font.Font(load_font("UbuntuSans-Regular.ttf"), 16)
    surface.blit(description_text.render(skill_group.cur_button.description, True, "black"),
                 (info.x + 15, info.y + 39))

    start_y = info.y + 100
    duration = 60

    for i in range(len(skill_group.buttons)):
        button = pygame.draw.rect(surface, skill_group.buttons[i].current_color, (66, start_y + i * duration, 392, 50),
                                  0, 5)
        skill_name = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 20)
        surface.blit(skill_name.render(skill_group.buttons[i].text, True, skill_group.buttons[i].current_text),
                     (button.x + 15, button.y + 15))

        skill_name = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 20)
        surface.blit(skill_name.render(f"{skill_group.buttons[i].item.mp} {get_string("mp")}", True,
                                       skill_group.buttons[i].current_text),
                     (button.size[0] - 15, button.y + 15))

    return surface


def draw_items(item_group):
    surface = pygame.surface.Surface(Data.get_screen_size(), pygame.SRCALPHA, 32)
    screen_size = Data.get_screen_size()
    panel = pygame.draw.rect(surface, "#ECECEC", (42, screen_size[1] // 3, 440, 605), 0, 15)

    title = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 32)
    surface.blit(title.render(get_string("use_item"), True, "black"),
                 (panel.x + 24, panel.y + 24))

    info = pygame.draw.rect(surface, "white", (panel.x + 24, panel.y + 76, 392, 87), 0, 5)
    name_text = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 20)
    surface.blit(name_text.render(item_group.cur_button.text, True, "black"),
                 (info.x + 15, info.y + 15))
    description_text = pygame.font.Font(load_font("UbuntuSans-Regular.ttf"), 16)
    surface.blit(description_text.render(item_group.cur_button.description, True, "black"),
                 (info.x + 15, info.y + 39))

    start_y = info.y + 100
    duration = 60

    for i in range(len(item_group.buttons)):
        button = pygame.draw.rect(surface, item_group.buttons[i].current_color, (66, start_y + i * duration, 392, 50),
                                  0, 5)
        skill_name = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 20)
        surface.blit(skill_name.render(item_group.buttons[i].text, True, item_group.buttons[i].current_text),
                     (button.x + 15, button.y + 15))

        skill_name = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 20)
        surface.blit(skill_name.render(str(item_group.buttons[i].item.count), True,
                                       item_group.buttons[i].current_text),
                     (button.size[0] - 15, button.y + 15))

    return surface


def draw_hp(character, x, y, screen):
    pygame.draw.rect(screen, "black", (x + 2, y + 2, 72, 15))
    pygame.draw.rect(screen, "gray", (x, y, 72, 15))
    pygame.draw.rect(screen, "yellow", (x, y, character.cur_health / character.health * 72, 15))
    pygame.draw.rect(screen, "black", (x, y, 72, 15), 2)


def draw_mp(character, x, y, screen):
    pygame.draw.rect(screen, "black", (x + 2, y + 2, 72, 15))
    pygame.draw.rect(screen, "gray", (x, y, 72, 15))
    pygame.draw.rect(screen, "purple", (x, y, character.cur_mana / character.mana * 72, 15))
    pygame.draw.rect(screen, "black", (x, y, 72, 15), 2)


def draw_target_select():
    surface = pygame.surface.Surface(Data.get_screen_size(), pygame.SRCALPHA, 32)
    screen_size = Data.get_screen_size()

    title = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 64)
    surface.blit(title.render(get_string("select_target"), True, "white"),
                 (64, screen_size[1] - 128))

    return surface


def draw_buttons(*buttons):
    surface = pygame.Surface(Data.get_screen_size(), pygame.SRCALPHA, 32)
    for i in range(len(buttons)):
        buttons[i].draw(32, surface.size[1] - 64 - i * 52, surface)

    return surface


def draw_battle_ui(current_ui, group, battle_icons, skill_group, item_group):
    match current_ui:
        case "buttons":

            return draw_battle_buttons(group, battle_icons), draw_buttons(
                Hint("action_selection", "Q", "E"),
                Hint("target_selection", "A", "D"),
                Hint("select", "Space"))
        case "skills":
            return draw_skills(skill_group), draw_buttons(Hint("back", "Esc"))
        case "items":
            return draw_items(item_group), draw_buttons(Hint("back", "Esc"))
        case "target":
            return draw_target_select(), draw_buttons(Hint("back", "Esc"))
