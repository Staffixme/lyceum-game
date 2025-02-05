import pygame
import os
import sys
import math

import save_data
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
        else:
            self.buttons = list()

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


class ListButton(Button):
    def __init__(self, text: str, size=64):
        super().__init__()
        self.text = text
        self.size = size
        self.opacity = 128

    def set_active(self):
        self.opacity = 255

    def set_inactive(self):
        self.opacity = 128


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
    surface = pygame.surface.Surface(save_data.Data.get_screen_size(), pygame.SRCALPHA, 32)
    bubble_surface = pygame.surface.Surface((450, 150), pygame.SRCALPHA, 32)
    pygame.draw.rect(bubble_surface, "#EEEEEE", (0, 0, 450, 150))
    bubble_surface = pygame.transform.rotate(bubble_surface, -25)
    surface.blit(bubble_surface, (surface.width - 390, -150))
    name_text = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 32)
    surface.blit(name_text.render(name, True, "black"), (surface.width - 150, 32))
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
    surface.blit(tooltip.render(group.cur_button.text, True, "white"),
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


def draw_list_buttons(group, screen, start_x, start_y, distance=92):
    for i in range(len(group.buttons)):
        button_text = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), group.buttons[i].size)
        button = button_text.render(group.buttons[i].text, True, "white")
        button.set_alpha(group.buttons[i].opacity)

        screen.blit(button, (start_x, start_y + distance * i))


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


def draw_shield(x, y, screen):
    shield_group = pygame.sprite.Group()
    icon = Icon("defense_icon.png", (42, 42))
    icon.rect.x = x
    icon.rect.y = y
    shield_group.add(icon)
    shield_group.draw(screen)


def draw_blue_rect(screen):
    rect = (0, 0, 800, screen.size[1])
    surface = pygame.surface.Surface((800, screen.size[1]), pygame.SRCALPHA, 32)
    pygame.draw.rect(surface, "#2B53AA", rect)
    surface = pygame.transform.rotate(surface, 125)

    screen.blit(surface, (screen.size[0] - screen.size[0] // 2 + 128, 485))


def draw_item_info_rect(screen, item_name, item_desc, cnt, character):
    rect = (screen.size[0] - screen.size[0] // 3 - 64, 0, 800, screen.size[1])
    surface = pygame.surface.Surface((800, screen.size[1]), pygame.SRCALPHA, 32)
    name = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 42)
    name_render = name.render(item_name, True, "white")
    count = pygame.font.Font(load_font("UbuntuSans-Regular.ttf"), 24)
    count_render = count.render(f"{get_string("you_have")}: {cnt}", True, "white")
    desc = pygame.font.Font(load_font("UbuntuSans-Regular.ttf"), 32)
    character_font = pygame.font.Font(load_font("UbuntuSans-Regular.ttf"), 32)
    character_render = character_font.render(f"{get_string("selected_ally")}:\n{character}", True,
                                             "white")

    desc_surface = pygame.surface.Surface((screen.size[0] // 4, screen.size[0] // 2), pygame.SRCALPHA, 32)
    words = [word.split(' ') for word in item_desc.splitlines()]  # 2D array where each row is a list of words.
    space = desc.size(' ')[0] + 5  # The width of a space.
    max_width, max_height = screen.size[0] // 4, screen.size[0] // 2
    x, y = 0, 0
    for line in words:
        for word in line:
            word_surface = desc.render(word, True, "white")
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width - 32:
                x = 0  # Reset the x.
                y += word_height + 5  # Start on new row.
            desc_surface.blit(word_surface, (x, y))
            x += word_width + space
        x = 0  # Reset the x.
        y += word_height

    pygame.draw.rect(screen, "#2B53AA", rect)
    screen.blit(name_render, (screen.size[0] - screen.size[0] // 3 - 32, 42))
    screen.blit(count_render, (screen.size[0] - screen.size[0] // 3 - 32, 100))
    screen.blit(desc_surface, (screen.size[0] - screen.size[0] // 3 - 32, 152))
    screen.blit(character_render, (screen.size[0] - screen.size[0] // 3 - 32, screen.size[1] - 400))


def print_stage(stage_num):
    button_text = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 32)
    text = button_text.render(f"{get_string("stage")}: {stage_num}", True, "white")

    return text
