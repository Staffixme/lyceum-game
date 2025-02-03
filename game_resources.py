import pygame
import os
import sys
from translatable_text import get_string


class Background(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__(BACKGROUNDS)
        self.image = image
        self.rect = pygame.rect.Rect(0, 0, 1920, 1080)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', 'images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_font(name):
    font = os.path.join('data', 'fonts', name)
    if not os.path.isfile(font):
        print(f"Файл с шрифтом '{font}' не найден")
        sys.exit()
    return font


def load_audio(name):
    audio = os.path.join('data', 'music', name)
    if not os.path.isfile(audio):
        print(f"Файл с аудио '{audio}' не найден")
        sys.exit()
    return audio


BACKGROUNDS = pygame.sprite.Group()
background = Background(load_image("dungeon_bg.png"))


class Icon(pygame.sprite.Sprite):
    def __init__(self, img: str, size: tuple):
        super().__init__()
        self.image = load_image(img)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()


class CharacterIcon:
    def __init__(self, img):
        self.icon = Icon(img, (180, 180))

    def draw_hp_bar(self, screen, x, y, width, height, cur_hp, hp):
        name = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 22)
        screen.blit(name.render(f"{get_string("hp")}: {cur_hp}/{hp}", True, "yellow"), (x, y - 28))

        pygame.draw.rect(screen, "black", (x + 2, y + 2, width, height))
        pygame.draw.rect(screen, "gray", (x, y, width, height))
        pygame.draw.rect(screen, "yellow", (x, y, cur_hp / hp * width, height))
        pygame.draw.rect(screen, "black", (x, y, width, height), 2)

    def draw_mp_bar(self, screen, x, y, width, height, cur_mana, mana):
        name = pygame.font.Font(load_font("UbuntuSans-SemiBold.ttf"), 22)
        screen.blit(name.render(f"{get_string("mp")}: {cur_mana}/{mana}", True, "white"), (x, y - 28))

        pygame.draw.rect(screen, "black", (x + 2, y + 2, width, height))
        pygame.draw.rect(screen, "gray", (x, y, width, height))
        pygame.draw.rect(screen, "white", (x, y, cur_mana / mana * width, height))
        pygame.draw.rect(screen, "black", (x, y, width, height), 2)


CHARACTERS_PORTRAITS = {
    "Knight": CharacterIcon("knight_portrait.png"),
    "Kunoichi": CharacterIcon("kunoichi_portrait.png"),
    "Dummy2": CharacterIcon("dummy_portrait.png"),
    "Dummy3": CharacterIcon("dummy_portrait.png")
}
