from settings import *
from map import world_map

import pygame
import math


class Player:
    def __init__(self):
        self.x, self.y = player_pos
        self.position = [self.x, self.y]
        self.delta_movement = [0, 0]
        self.movement_speed = 20

        self.angle = player_angle
        self.rotate = player_angle
        self.delta_rotate = 0
        self.rotate_speed = 20

        self.last_time = pygame.time.get_ticks()

    @property
    def pos(self):
        return (self.x, self.y)

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        keys = pygame.key.get_pressed()

        if pygame.time.get_ticks() - self.last_time > 550:

            if keys[pygame.K_w]:
                pos = [self.position[0] + TILE * cos_a, self.position[1] + TILE * sin_a]
                if not check_wall(world_map, pos):
                    self.position = pos
                    self.correction_move()
            if keys[pygame.K_s]:
                self.rotate += 1.58 * 2
                self.rotate %= 6.320001
                self.rotate = round(self.rotate, 2)
                self.correction_move()
            if keys[pygame.K_a]:
                self.rotate -= 1.58
                self.rotate %= 6.320001
                self.rotate = round(self.rotate, 2)
                self.correction_move()
                print(self.rotate)
            if keys[pygame.K_d]:
                self.rotate += 1.58
                self.rotate %= 6.320001
                self.rotate = round(self.rotate, 2)
                self.correction_move()
                print(self.rotate)

        if self.angle < self.rotate:
            self.angle += self.delta_rotate / self.rotate_speed
            if self.rotate - self.angle < 0.01:
                self.angle = self.rotate
                if self.rotate == 6.32:
                    self.rotate = player_angle
                    self.angle = player_angle
        elif self.angle > self.rotate:
            self.angle -= self.delta_rotate / self.rotate_speed
            if self.angle - self.rotate < 0.01:
                self.angle = self.rotate
                if self.rotate == 6.32:
                    self.rotate = player_angle
                    self.angle = player_angle

        # movement
        if not self.x == self.position[0]:
            if self.x < self.position[0]:
                self.x += self.delta_movement[0] / self.movement_speed
            elif self.x > self.position[0]:
                self.x -= self.delta_movement[0] / self.movement_speed

        if not self.y == self.position[1]:
            if self.y < self.position[1]:
                self.y += self.delta_movement[1] / self.movement_speed
            if self.y > self.position[1]:
                self.y -= self.delta_movement[1] / self.movement_speed

    def correction_move(self):
        self.last_time = pygame.time.get_ticks()

        self.x = rounding_up_coordinates(self.x)
        self.y = rounding_up_coordinates(self.y)
        self.position[0] = rounding_up_coordinates(self.position[0])
        self.position[1] = rounding_up_coordinates(self.position[1])

        self.delta_rotate = abs(self.angle - self.rotate)
        self.delta_movement = [abs(self.x - self.position[0]), abs(self.y - self.position[1])]


def rounding_up_coordinates(i):
    i = int(i)
    original_number = i
    i = original_number - (original_number % 1000)
    n = (original_number - i) // 10

    if (n % 10) <= 2.5:
        n = n // 10 * 100
    elif 2.5 < (n % 10) <= 5:
        n = n // 10 * 100 + 50
    elif 5 < (n % 10) <= 7.5:
        n = n // 10 * 100 + 50
    elif (n % 10) > 7.5:
        n = (n // 10 + 1) * 100

    return i + n


def check_wall(this_map, position):
    for tile in this_map:
        if tile[0] < position[0] < tile[0] + 100 and tile[1] < position[1] < tile[1] + 100:
            return True
    return False


def check_event(this_map, position):
    for tile in this_map:
        if tile[0] < position[0] < tile[0] + 100 and tile[1] < position[1] < tile[1] + 100:
            return True
    return False
