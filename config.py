from typing import List
import math

"""
Павлов Тимур:
26.12.2021. Созданы константы
28.12.2021. Внесены поправки
01.01.2021. Добавлены настройки проекции

Вайман Ангелина:
28.12.2021. Внесены поправки
03.01.2022. Добавлены настройки миникарты и новые цвета
"""

# Настройки экрана
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (1200, 600)
HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT = SCREEN_WIDTH >> 1, SCREEN_HEIGHT >> 1
WINDOW_NAME = 'Game'

# Настройки игрока и луча
FPS = 120
PLAYER_SPEED = 2
SENSITIVITY = 0.005
MAX_VIEW_DISTANCE = 800

# Настройки ray casting
FOV = math.pi / 3
HALF_FOV = FOV / 2
RAYS_AMOUNT = 300
MAX_RAY_DISTANCE = 800
DELTA_ANGLE = FOV / RAYS_AMOUNT

# Карта и настройки карты
MAP: List[str] = [
    '11111111111111111111111111111111',
    '1..............................1',
    '1.222......1...1.1...1.....222.1',
    '1.222......11111.11111.....222.1',
    '1.....212..............212.....1',
    '1.222......11111.11111.....222.1',
    '1.222......1...1.1...1.....222.1',
    '1..............................1',
    '1.11111..................11111.1',
    '1.11111..................11111.1',
    '1.11111.......22222......11111.1',
    '1.............22222............1',
    '1.............22222............1',
    '1..11111......22222......11111.1',
    '1..11111.................11111.1',
    '1..11111.................11111.1',
    '1..............................1',
    '1.222......1...1.1...1.....222.1',
    '1.222......11111.11111.....222.1',
    '1.....212..............212.....1',
    '1.222......11111.11111.....222.1',
    '1.222......1...1.1...1.....222.1',
    '1..............................1',
    '11111111111111111111111111111111'
]
WALL_CHARS = ('1', '2')
TILE = 64
WORLD_MAP = set()
MAP_SIZE = (len(MAP[0]), len(MAP))

# Цвета
ORANGE = 'Orange'
PURPLE = 'Purple'
BLACK = 'Black'
SKYBLUE = 'Skyblue'
DARKGREY = 'Darkgrey'
YELLOW = 'Yellow'
GREEN = 'Green'
RED = 'Red'
WHITE = 'White'

# Расстояние до краев клетки
RIGHT = 0
LEFT = 1
BOTTOM = 2
TOP = 3

# Настройки проекции
SCALE = SCREEN_WIDTH // RAYS_AMOUNT
DISTANCE_TO_PROJECTION_PLANE = RAYS_AMOUNT / (2 * math.tan(HALF_FOV))
PROJECTION_COEFFICIENT = TILE * DISTANCE_TO_PROJECTION_PLANE * 5

# Настройки миникарты
MINI_MAP = set()
MAP_SCALE = 5
MAP_TILE = SCREEN_HEIGHT / MAP_SIZE[1] // MAP_SCALE
