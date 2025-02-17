import pygame
import settings
from ray_casting import ray_casting
from map import mini_map, door_map
from save_data import Data


class Drawing:
    def __init__(self):
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = {"1": pygame.image.load('lyceum-game-main/texture/wall_1.png').convert(),
                         '2': pygame.image.load('lyceum-game-main/texture/wall_2.png').convert(),
                         'B': pygame.image.load('lyceum-game-main/sprites/box_1.png').convert(),
                         'E': pygame.image.load('lyceum-game-main/sprites/enemy_1.png').convert(),
                         '!': pygame.image.load('lyceum-game-main/texture/door_3.png').convert(),

                         'S': pygame.image.load('lyceum-game-main/texture/sky_3.png').convert(),
                         'M': pygame.image.load('lyceum-game-main/texture/Floor_1.png').convert(),
                         }

    def background(self, screen, angle):
        sky_offset = -8 * settings.math.degrees(angle) % settings.WIDTH

        screen.blit(pygame.transform.scale(self.textures['S'], (settings.WIDTH, settings.HEIGHT)), (sky_offset, 0))
        screen.blit(pygame.transform.scale(self.textures['S'], (settings.WIDTH, settings.HEIGHT)), (sky_offset - settings.WIDTH, 0))
        screen.blit(pygame.transform.scale(self.textures['S'], (settings.WIDTH, settings.HEIGHT)), (sky_offset + settings.WIDTH, 0))

        pygame.draw.rect(screen, settings.DARKGRAY, (0, settings.HALF_HEIGHT, settings.WIDTH, settings.HALF_HEIGHT))

    def world(self, screen, player_pos, player_angle):
        ray_casting(screen, player_pos, player_angle, self.textures)

    def fps(self, screen, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, settings.RED)
        screen.blit(render, settings.FPS_POS)

    def mini_map(self, player):
        sc_map = pygame.Surface((Data.get_screen_size()[0] // settings.MAP_SCALE, Data.get_screen_size()[1] // settings.MAP_SCALE), pygame.SRCALPHA, 32)
        map_x, map_y = player.x // settings.MAP_SCALE, player.y // settings.MAP_SCALE
        pygame.draw.line(sc_map, "yellow", (map_x, map_y), (map_x + 12 * settings.math.cos(player.angle),
                                                 map_y + 12 * settings.math.sin(player.angle)), 2)
        pygame.draw.circle(sc_map, "blue", (int(map_x), int(map_y)), 3)
        for x, y in mini_map:
            pygame.draw.rect(sc_map, "orange", (x, y, settings.MAP_TILE, settings.MAP_TILE))
        return sc_map
