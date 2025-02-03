import pygame
import settings
from ray_casting import ray_casting
from map import mini_map
from save_data import Data


class Drawing:
    def __init__(self, sc_map):
        self.sc_map = sc_map
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = {"1": pygame.image.load('lyceum-game-main/texture/wall_1.png').convert(),
                         '2': pygame.image.load('lyceum-game-main/texture/wall_2.png').convert(),
                         'B': pygame.image.load('lyceum-game-main/sprites/box_1.png').convert(),
                         'E': pygame.image.load('lyceum-game-main/sprites/enemy_1.png').convert(),

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

    def mini_map(self, screen, player):
        self.sc_map.fill(settings.BLACK)
        map_x, map_y = player.x // settings.MAP_SCALE, player.y // settings.MAP_SCALE
        pygame.draw.line(self.sc_map, settings.YELLOW, (map_x, map_y), (map_x + 12 * settings.math.cos(player.angle),
                                                 map_y + 12 * settings.math.sin(player.angle)), 2)
        pygame.draw.circle(self.sc_map, settings.RED, (int(map_x), int(map_y)), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.sc_map, settings.SANDY, (x, y, settings.MAP_TILE, settings.MAP_TILE))
        screen.blit(self.sc_map, settings.MAP_POS)
