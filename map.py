from settings import *
import random
import global_events

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


for j, row in enumerate(levels[global_events.number_lvl]):
    row_list = list(row)
    for i, char in enumerate(row):
        if levels[global_events.number_lvl][j][i] == 'E':
            row_list[i] = '.'
    levels[global_events.number_lvl][j] = ''.join(row_list)


for j, row in enumerate(levels[global_events.number_lvl]):
    row_list = list(row)
    for i, char in enumerate(row_list):
        if char == '.':
            probability = random.randint(global_events.number_lvl, 100)
            if probability > 80:
                row_list[i] = 'E'
    levels[global_events.number_lvl][j] = ''.join(row_list)


for j, row in enumerate(levels[global_events.number_lvl]):
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

