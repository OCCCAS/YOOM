import pygame

from config import *
from point import Point
from ray import Ray
from sound import SoundEffect

"""
Павлов Тимур 26.12.2021. Создан класс Player

Батталов Арслан 03.01.2022. Изменена функция _process_keyboard, добавлены функции find_collison, change_cors
(пока не отлажено)

Батталов Арслан 04.01.2022. Добавлена функция can_move
Батталов Арслан 05.01.2022. Добавлены функции sound_effect_init, sound
"""


class Player:
    def __init__(self, x, y):
        self._x, self._y = x, y
        self.direction = 0
        self.player_collision = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SPEED)
        self.collision_map = COLLISION_MAP
        self.footstep_sound = SoundEffect(FOOTSTEP)
        self.shot = False
        self.gun = 1

    def update(self):
        self._process_mouse()
        self._process_keyboard()
        self.sound()
        self.player_collision.center = self._x, self._y

    @property
    def pos(self) -> Point:
        return Point(self._x, self._y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def _process_keyboard(self):
        pressed_keys = pygame.key.get_pressed()

        cos_a, sin_a = math.cos(self.direction), math.sin(self.direction)

        if pressed_keys[pygame.K_w]:
            if self.can_move(self.direction, PLAYER_SIZE * 4):
                self._x += cos_a * PLAYER_SPEED
                self._y += sin_a * PLAYER_SPEED
        if pressed_keys[pygame.K_s]:
            if self.can_move(self.direction - math.pi, PLAYER_SIZE * 4):
                self._x += -cos_a * PLAYER_SPEED
                self._y += -sin_a * PLAYER_SPEED
        if pressed_keys[pygame.K_a]:
            if self.can_move(self.direction - math.pi / 2, PLAYER_SIZE * 3):
                self._x += sin_a * PLAYER_SPEED
                self._y += -cos_a * PLAYER_SPEED
        if pressed_keys[pygame.K_d]:
            if self.can_move(self.direction + math.pi / 2, PLAYER_SIZE * 3):
                self._x += -sin_a * PLAYER_SPEED
                self._y += cos_a * PLAYER_SPEED
        if pressed_keys[pygame.K_LEFT]:
            self.direction -= SENSITIVITY
        if pressed_keys[pygame.K_RIGHT]:
            self.direction += SENSITIVITY
        if pressed_keys[pygame.K_1]:
            self.gun = 1
        if pressed_keys[pygame.K_2]:
            self.gun = 2
        if pressed_keys[pygame.K_3]:
            self.gun = 3

    def _process_mouse(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_SCREEN_WIDTH
            pygame.mouse.set_pos((HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT))
            self.direction += difference * SENSITIVITY
            self.direction %= math.radians(360)

    def can_move(self, direction, collision_distance):
        ray = Ray(self.pos, direction, MAX_RAY_DISTANCE)

        if ray.ray_cast().distance <= collision_distance:
            return False

        return True

    def sound(self):
        pressed_keys = pygame.key.get_pressed()

        if (pressed_keys[pygame.K_w] or pressed_keys[pygame.K_s]
                or pressed_keys[pygame.K_a] or pressed_keys[pygame.K_d]):
            self.footstep_sound.play_sound()
