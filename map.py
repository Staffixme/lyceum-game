from settings import *
import random
from save_data import current_data

levels = [
    [
        '11111111111111',
        '1.....1...1..1',
        '1..1..111.11.1',
        '1.11...1...1.1',
        '1....1.......1',
        '1.111...11...1',
        '1......11..!11',
        '1..1....1..111',
        '11111111111111'
    ],
    [
        '11111111111111',
        '1.....11.....1',
        '1......1..11.1',
        '1.1.11.....1.1',
        '1111111..1...1',
        '1..11...111..1',
        '1..1.....1...1',
        '1!.........1.1',
        '11111111111111'
    ],
    [
        '11111111111111',
        '1........1...1',
        '1...11.111.111',
        '1..11...1...11',
        '11....!.1....1',
        '1..1....1.11.1',
        '1..111....11.1',
        '1............1',
        '11111111111111',

    ]
]

lvl1 = [
    '11111111111111',
    '1.!...1...1..1',
    '1..1..111.11.1',
    '1.11...1...1.1',
    '1....1.......1',
    '1.111...11...1',
    '1......11..!11',
    '1..1....1..111',
    '11111111111111'
]

world_map = {}
event_map = {}
door_map = {}

mini_map = set()


def generate_stage():
    global world_map, event_map, door_map, mini_map
    world_map.clear()
    event_map.clear()
    door_map.clear()
    mini_map.clear()
    for j, row in enumerate(levels[current_data.stage % 3]):
        row_list = list(row)
        for i, char in enumerate(row):
            if levels[current_data.stage % 3][j][i] == 'E':
                row_list[i] = '.'
        levels[current_data.stage % 3][j] = ''.join(row_list)

    for j, row in enumerate(levels[current_data.stage % 3]):
        row_list = list(row)
        for i, char in enumerate(row_list):
            if char == '.':
                probability = random.randint(current_data.stage, 100)
                if probability > 85:
                    row_list[i] = 'E'
        levels[current_data.stage % 3][j] = ''.join(row_list)

    for j, row in enumerate(levels[current_data.stage % 3]):
        for i, char in enumerate(row):
            if char == 'E':
                event_map[(i * TILE, j * TILE)] = 'E'
            elif char == '!':
                door_map[(i * TILE, j * TILE)] = '!'
            elif char != '.':
                mini_map.add((i * MAP_TILE, j * MAP_TILE))
                if char == '1':
                    world_map[(i * TILE, j * TILE)] = '1'
                elif char == '2':
                    world_map[(i * TILE, j * TILE)] = '2'
