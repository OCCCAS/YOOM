from typing import List
import math
from load_image import load_image

"""
Павлов Тимур:
26.12.2021. Созданы константы
28.12.2021. Внесены поправки
01.01.2021. Добавлены настройки проекции

Вайман Ангелина:
28.12.2021. Внесены поправки
03.01.2022. Добавлены настройки миникарты и новые цвета

Батталов Арслан:
03.01.2021. Добавлены константы для коллизии
"""

# Настройки экрана
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (1200, 600)
HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT = SCREEN_WIDTH >> 1, SCREEN_HEIGHT >> 1
WINDOW_NAME = 'Game'

# Настройки игрока и луча
FPS = 120
PLAYER_SPEED = 1
SENSITIVITY = 0.005
MAX_VIEW_DISTANCE = 800
PLAYER_SIZE = 20
MAX_DISTANCE_TO_WALL = 10

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
TILE = 25
WORLD_MAP = set()
MAP_SIZE = (len(MAP[0]), len(MAP))
COLLISION_MAP = list()

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
BRICK = (139, 79, 57)

# Настройки проекции
SCALE = SCREEN_WIDTH // RAYS_AMOUNT
DISTANCE_TO_PROJECTION_PLANE = RAYS_AMOUNT / (2 * math.tan(HALF_FOV))
PROJECTION_COEFFICIENT = TILE * DISTANCE_TO_PROJECTION_PLANE * 3

# Настройки миникарты
MINI_MAP = set()
MAP_SCALE = 5
MAP_TILE = SCREEN_HEIGHT / MAP_SIZE[1] // MAP_SCALE

# Текстуры
SKY_TEXTURE = 'sky.png'
WALL_TEXTURE = load_image('wall.png')