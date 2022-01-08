from copy import deepcopy
from config import TILE, SPRITE_CHARS, MAP, TEXTURE_FILE, STATIC_SPRITES, MOVABLE_SPRITES, MAP_SIZE
from load_image import load_image
from utils import world_pos2cell

"""
Павлов Тимур 08.01.2022. Создан класс Sprite и функция create_sprites
"""

sprite_textures = {
    '3': load_image(TEXTURE_FILE, 'plant.png'),
    '4': load_image(TEXTURE_FILE, 'barrel.png'),
    '5': load_image(TEXTURE_FILE, 'enemy.png')
}
sprite_speed = 5


class Sprite:
    def __init__(self, texture, pos):
        self.texture = texture
        self.pos = self.x, self.y = list(pos)


class MovableSprite(Sprite):
    def __init__(self, texture, pos, speed):
        super(MovableSprite, self).__init__(texture, pos)
        self.speed = speed

        self._current_route = []
        self._steps_to_end_route = -1

        self._ticks = 0
        self._to_x, self._to_y = -1, -1
        self._dx, self._dy = 0, 0

    @staticmethod
    def _get_clean_board():
        return [[0 for _ in range(MAP_SIZE[0])] for _ in range(MAP_SIZE[1])]

    def move_to(self, to_x, to_y):
        if int(self._to_x) != int(to_x // TILE) or int(self._to_y) != int(to_y // TILE):
            self._current_route = []

        if not self._current_route:
            from_x, from_y = world_pos2cell(*self.pos)
            to_x, to_y = world_pos2cell(to_x, to_y)
            wave_map = self.has_path(from_x, from_y, to_x, to_y)
            self._to_x, self._to_y = to_x, to_y

            if wave_map:
                route = self.get_route_to_point(wave_map, to_x, to_y)
                self._current_route = deepcopy(route)
                self.set_delta_move()
        else:
            if self.pos[0] // TILE == self._current_route[0][0] * TILE \
                    and self.pos[1] // TILE == self._current_route[0][1] * TILE:
                self.set_delta_move()
                self._current_route = self._current_route[1:]
            else:
                self.pos[0] += self._dx * self.speed
                self.pos[1] += self._dy * self.speed

    def has_path(self, x0, y0, x1, y1):
        wave_map = self._get_clean_board()
        wave_map[y0][x0] = 1

        current_step = 1
        while wave_map[y1][x1] == 0:
            previous_wave_map = deepcopy(wave_map)
            wave_map = self._next_step(wave_map, current_step)

            if previous_wave_map == wave_map:
                return

            current_step += 1

        return wave_map

    @staticmethod
    def get_route_to_point(wave_map, to_x, to_y):
        k = wave_map[to_y][to_x]
        route = [(to_x, to_y)]
        while k > 1:
            if to_y > 0 and wave_map[to_y - 1][to_x] == k - 1:
                to_y, to_x = to_y - 1, to_x
                route.append((to_x, to_y))
                k -= 1
            elif to_y < MAP_SIZE[1] - 1 and wave_map[to_y + 1][to_x] == k - 1:
                to_y, to_x = to_y + 1, to_x
                route.append((to_x, to_y))
                k -= 1
            elif to_x > 0 and wave_map[to_y][to_x - 1] == k - 1:
                to_y, to_x = to_y, to_x - 1
                route.append((to_x, to_y))
                k -= 1
            elif to_x < MAP_SIZE[0] - 1 and wave_map[to_y][to_x + 1] == k - 1:
                to_y, to_x = to_y, to_x + 1
                route.append((to_x, to_y))
                k -= 1

        return route[::-1]

    def set_delta_move(self):
        if len(self._current_route) > 1:
            self._dx = self._current_route[1][0] - self._current_route[0][0]
            self._dy = self._current_route[1][1] - self._current_route[0][1]
        else:
            self._dx, self._dy = 0, 0

    @staticmethod
    def _next_step(map_, current_step):
        for i in range(MAP_SIZE[1]):
            for j in range(MAP_SIZE[0]):
                if map_[i][j] == current_step:
                    if i > 0 and map_[i - 1][j] == 0 and MAP[i - 1][j] == '.':
                        map_[i - 1][j] = current_step + 1
                    if j > 0 and map_[i][j - 1] == 0 and MAP[i][j - 1] == '.':
                        map_[i][j - 1] = current_step + 1
                    if i < MAP_SIZE[1] - 1 and map_[i + 1][j] == 0 and MAP[i + 1][j] == '.':
                        map_[i + 1][j] = current_step + 1
                    if j < MAP_SIZE[0] - 1 and map_[i][j + 1] == 0 and MAP[i][j + 1] == '.':
                        map_[i][j + 1] = current_step + 1

        return map_


def create_sprites() -> list[Sprite]:
    sprites = []

    for row_index, row in enumerate(MAP):
        for col_index, el in enumerate(row):
            if el in SPRITE_CHARS:
                x, y = col_index * TILE + TILE // 2, row_index * TILE + TILE // 2
                texture = sprite_textures[el]

                if el in STATIC_SPRITES:
                    sprite = Sprite(texture, (x, y))
                    sprites.append(sprite)
                elif el in MOVABLE_SPRITES:
                    sprite = MovableSprite(texture, (x, y), sprite_speed)
                    sprites.append(sprite)

    return sprites
