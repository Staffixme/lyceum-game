from settings import *
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
                self.position = [self.position[0] + TILE * cos_a, self.position[1] + TILE * sin_a]
                self.correction_move()
            if keys[pygame.K_s]:
                if DIRECTIONS[self.angle] == "ahead":
                    self.rotate = 3.14
                elif DIRECTIONS[self.angle] == "behind":
                    self.rotate = 0
                elif DIRECTIONS[self.angle] == "left":
                    self.rotate = 1.56
                elif DIRECTIONS[self.angle] == "right":
                    self.rotate = 4.72
                self.correction_move()
            if keys[pygame.K_a]:
                if DIRECTIONS[self.angle] == "ahead":
                    self.rotate = 4.72
                elif DIRECTIONS[self.angle] == "behind":
                    self.rotate = 1.56
                elif DIRECTIONS[self.angle] == "left":
                    self.rotate = 3.14
                elif DIRECTIONS[self.angle] == "right":
                    self.rotate = 0
                self.correction_move()
            if keys[pygame.K_d]:
                if DIRECTIONS[self.angle] == "ahead":
                    self.rotate = 1.56
                elif DIRECTIONS[self.angle] == "behind":
                    self.rotate = 4.72
                elif DIRECTIONS[self.angle] == "left":
                    self.rotate = 0
                elif DIRECTIONS[self.angle] == "right":
                    self.rotate = 3.14
                self.correction_move()

        if self.angle < self.rotate:
            self.angle += self.delta_rotate / self.rotate_speed
            if self.rotate - self.angle < 0.01:
                self.angle = self.rotate
        elif self.angle > self.rotate:
            self.angle -= self.delta_rotate / self.rotate_speed
            if self.angle - self.rotate < 0.01:
                self.angle = self.rotate

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

    print(i + n)
    return i + n
