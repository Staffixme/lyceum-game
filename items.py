import random
from game_resources import load_image, CHARACTERS_PORTRAITS
import pygame
from translatable_text import get_string


class Melee:
    def __init__(self, name: str, damage: int):
        self.name = name
        self.damage = damage


class Skill:
    def __init__(self, name: str, description: str, mp: int):
        self.name = name
        self.description = description
        self.type = type
        self.mp = mp

    def use_skill(self, target):
        pass


class AttackSkill(Skill):
    def __init__(self, name, description: str, attack: int, is_group_use: bool, mp: int):
        super().__init__(name, description, mp)
        self.attack = attack
        self.is_group_use = is_group_use

    def use_skill(self, target):
        if not self.is_group_use:
            target.get_damage(self.attack)
        elif self.is_group_use:
            for i in target[1]:
                if i.is_alive:
                    i.get_damage(self.attack)


class HealSkill(Skill):
    def __init__(self, name, description: str, value: int, is_group_use: bool, mp: int):
        super().__init__(name, description, mp)
        self.value = value
        self.is_group_use = is_group_use

    def use_skill(self, target):
        if not self.is_group_use:
            target.heal(self.value)
        elif self.is_group_use:
            for i in target[0]:
                if i.is_alive:
                    i.heal(self.value)


class CharacterSprite(pygame.sprite.Sprite):
    def __init__(self, idle: tuple, attack: tuple, defence: tuple, skill_item: tuple, defeated: tuple):
        super().__init__(CHARACTERS_SPRITES)
        self.animation = "idle"
        self.idle_state = self.cut_sheet(*idle)
        self.attack_state = self.cut_sheet(*attack)
        self.skill_item_state = self.cut_sheet(*skill_item)
        self.defence_state = self.cut_sheet(*defence)
        self.defeated_state = self.cut_sheet(*defeated)
        self.is_play = False
        self.animation_index = 0
        self.image = self.idle_state[self.animation_index]
        self.rect = self.image.get_rect()

        self.current_time = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 100

    def cut_sheet(self, sprite, count):
        frames = list()

        self.rect = pygame.Rect(0, 0, sprite.get_width() // count,
                                sprite.get_height())

        for i in range(count):
            frame_location = (self.rect.w * i, 0)
            frame = sprite.subsurface(pygame.Rect(frame_location, self.rect.size))
            frame = pygame.transform.scale(frame, (256, 256))
            frames.append(frame)

        return frames

    def change_animation(self, name):
        self.animation_index = 0
        self.is_play = False
        self.animation = name

    def draw(self):
        self.current_time = pygame.time.get_ticks()

        if self.animation == "attack":
            frames_count = len(self.attack_state)
        elif self.animation == "skill" or self.animation == "item":
            frames_count = len(self.skill_item_state)
        elif self.animation == "defense":
            frames_count = len(self.defence_state)
        elif self.animation == "defeated":
            frames_count = len(self.defeated_state)
        else:
            frames_count = len(self.idle_state)

        if self.current_time - self.last_update > self.frame_delay:
            self.animation_index = (self.animation_index + 1) % frames_count
            self.last_update = self.current_time

        match self.animation:
            case "defeated":
                self.image = self.defeated_state[self.animation_index]
                if self.animation_index + 1 == frames_count and self.is_play:
                    self.is_play = False
                else:
                    self.is_play = True
            case "defense":
                self.image = self.defence_state[self.animation_index]
                if self.animation_index == 0 and self.is_play:
                    self.animation = "idle"
                    self.is_play = False
                else:
                    self.is_play = True
            case "idle":
                self.image = self.idle_state[self.animation_index]
            case "attack":
                self.image = self.attack_state[self.animation_index]
                if self.animation_index == 0 and self.is_play:
                    self.animation = "idle"
                    self.is_play = False
                else:
                    self.is_play = True
            case "skill":
                self.image = self.skill_item_state[self.animation_index]
                if self.animation_index == 0 and self.is_play:
                    self.animation = "idle"
                    self.is_play = False
                else:
                    self.is_play = True
            case "item":
                self.image = self.skill_item_state[self.animation_index]
                if self.animation_index == 0 and self.is_play:
                    self.animation = "idle"
                    self.is_play = False
                else:
                    self.is_play = True


class Character:
    def __init__(self, name: str, hp: int, weapon: Melee, skills: tuple, sprite: tuple):
        self.name = name
        self.health = hp
        self.cur_health = hp

        self.weapon = weapon
        self.skills = skills

        self.is_alive = True
        self.is_protected = False

        self.sprites = CharacterSprite(*sprite)

    def heal(self, value: int):
        self.cur_health += value
        if self.cur_health > self.health:
            self.cur_health = self.health

    def attack(self, target):
        target.get_damage(self.weapon.damage)

    def get_damage(self, value: int):
        if not self.is_protected:
            damage = value
        else:
            damage = value - value // 3
            self.is_protected = False
        self.cur_health -= damage
        print(f"{self.name} got {damage} damage")
        if self.cur_health <= 0:
            self.cur_health = 0
            self.is_alive = False
            self.sprites.change_animation("defeated")
            print(f"{self.name} is death")


class Hero(Character):
    def __init__(self, name: str, hp: int, mana: int, weapon: Melee, skills: tuple, equipment, sprite: tuple, portrait):
        super().__init__(name, hp, weapon, skills, sprite)
        self.mana = mana
        self.cur_mana = mana
        self.equipment = equipment
        self.portrait = portrait
        self.is_leader = False


class Enemy(Character):
    def __init__(self, name: str, hp: int, weapon, skills: tuple, sprite: tuple):
        super().__init__(name, hp, weapon, skills, sprite)


class Item:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.count = 0
        self.count += 1

    def use(self, target: Character | list):
        pass

    def __copy__(self):
        return Item(self.name, self.description)


class HealItem(Item):
    def __init__(self, name: str, description: str, value: int, is_group_use: bool):
        super().__init__(name, description)
        self.value = value
        self.is_group_use = is_group_use

    def use(self, target: Character | tuple):
        if not self.is_group_use:
            target.heal(self.value)
        elif self.is_group_use:
            for i in target[0]:
                if i.is_alive:
                    i.heal(self.value)
        self.count -= 1

    def __copy__(self):
        return HealItem(self.name, self.description, self.value, self.is_group_use)


class AttackItem(Item):
    def __init__(self, name: str, description: str, value: int, is_group_use: bool):
        super().__init__(name, description)
        self.value = value
        self.is_group_use = is_group_use

    def use(self, target: Character | tuple):
        if not self.is_group_use:
            target.get_damage(self.value)
        elif self.is_group_use:
            for i in target[0]:
                if i.is_alive:
                    i.get_damage(self.value)
        self.count -= 1

    def __copy__(self):
        return AttackItem(self.name, self.description, self.value, self.is_group_use)


CHARACTERS_SPRITES = pygame.sprite.Group()

SKILLS = {
    "Test_skill": AttackSkill("Атакующий навык", "Наносит большой урон одному врагу", 200,
                              False, 20),
    "Test_skill_group": AttackSkill("Массовый атакующий навык", "Наносит средний урон всем врагу",
                                    100, True, 25),
    "Heal_skill": HealSkill("Исцеление", "Исцеляет небольшое количество ОЗ одному союзнику", 50,
                            False, 5),
}

ITEMS = {
    "Aid": HealItem("Аптечка", "Исцеляет среднее количество ОЗ одному союзнику", 100, False),
    "Aid_kit": HealItem("Набор первой помощи", "Исцеляет большое количество ОЗ всем союзникам", 500, True),
    "Imba": AttackItem("Этот предмет просто имба", "Урон, мгновенно убивающий врага", 999999, False),
}

WEAPONS = {
    "Katana": Melee("Катана", 100),
    "Enemy_wp": Melee("Вражеское оружие", 30)
}

CHARACTERS = {
    "Dummy": Hero(get_string("dummy"), 2000, 50, WEAPONS["Katana"],
                  (SKILLS["Test_skill"], SKILLS["Test_skill_group"], SKILLS["Heal_skill"]),
                  None,
                  ((load_image("IDLE.png"), 7),
                   (load_image("ATTACK 1.png"), 6),
                   (load_image("DEFEND.png"), 6),
                   (load_image("JUMP.png"), 5),
                   (load_image("DEATH.png"), 12)),
                  CHARACTERS_PORTRAITS["Knight"]),
    "Dummy1": Hero(get_string("dummy"), 200, 50, WEAPONS["Enemy_wp"], (SKILLS["Test_skill"], SKILLS["Heal_skill"]),
                   None,
                   ((load_image("IDLE.png"), 7),
                    (load_image("ATTACK 1.png"), 6),
                    (load_image("DEFEND.png"), 6),
                    (load_image("JUMP.png"), 5),
                    (load_image("DEATH.png"), 12)),
                   CHARACTERS_PORTRAITS["Dummy1"]),
    "Dummy2": Hero(get_string("dummy"), 200, 50, WEAPONS["Katana"], (SKILLS["Test_skill"],), None,
                   ((load_image("IDLE.png"), 7),
                    (load_image("ATTACK 1.png"), 6),
                    (load_image("DEFEND.png"), 6),
                    (load_image("JUMP.png"), 5),
                    (load_image("DEATH.png"), 12)),
                   CHARACTERS_PORTRAITS["Dummy2"]),
    "Dummy3": Hero(get_string("dummy"), 200, 50, WEAPONS["Katana"], (SKILLS["Heal_skill"],), None,
                   ((load_image("IDLE.png"), 7),
                    (load_image("ATTACK 1.png"), 6),
                    (load_image("DEFEND.png"), 6),
                    (load_image("JUMP.png"), 5),
                    (load_image("DEATH.png"), 12)),
                   CHARACTERS_PORTRAITS["Dummy3"]),

}

ENEMIES = {
    "Dummy3": ("Враг 1", 200, WEAPONS["Katana"], (None,),
               ((load_image("IDLE.png"), 7),
                (load_image("ATTACK 1.png"), 6),
                (load_image("DEFEND.png"), 6),
                (load_image("JUMP.png"), 5),
                (load_image("DEATH.png"), 12))),
    "Dummy4": ("Враг 2", 200, WEAPONS["Enemy_wp"], (None,),
               ((load_image("IDLE.png"), 7),
                (load_image("ATTACK 1.png"), 6),
                (load_image("DEFEND.png"), 6),
                (load_image("JUMP.png"), 5),
                (load_image("DEATH.png"), 12))),
    "Dummy5": ("Враг 3", 200, WEAPONS["Enemy_wp"], (None,),
               ((load_image("IDLE.png"), 7),
                (load_image("ATTACK 1.png"), 6),
                (load_image("DEFEND.png"), 6),
                (load_image("JUMP.png"), 5),
                (load_image("DEATH.png"), 12))),
}


def create_enemy(name):
    return Enemy(*ENEMIES[name])


def get_item(name):
    return ITEMS[name].copy()
