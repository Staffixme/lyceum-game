from settings import *

text_map = [
    '111111111111',
    '1..E...1...1',
    '1..111...1.1',
    '1....1.E11.1',
    '1E.1....1..1',
    '1..1...111E1',
    '1..........1',
    '1111111111111'
]

world_map = {}
event_map = {}
mini_map = set()
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char == 'E':
            event_map[(i * TILE, j * TILE)] = 'E'
        elif char != '.':
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            if char == '1':
                world_map[(i * TILE, j * TILE)] = '1'
            elif char == '2':
                world_map[(i * TILE, j * TILE)] = '2'

