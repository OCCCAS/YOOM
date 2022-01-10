import pygame

from config import *
from point import Point
from ray import Ray
from ray_casting import sprites_ray_casting
from sound import GunSound, SpritesSound
from sprite import MovableSprite
from weapon import Weapon

"""
Павлов Тимур 26.12.2021. Создан класс Player

Батталов Арслан 03.01.2022. Изменена функция _process_keyboard, добавлены функции find_collision, change_cors
(пока не отлажено)

Батталов Арслан 04.01.2022. Добавлена функция can_move
Батталов Арслан 05.01.2022. Добавлены функции sound_effect_init, sound

Вайман Ангелина 06.01.2022. Добавлены функции _shot

Павлов Тимур 09.01.2022. Добавлена функция do_shot
Павлов Тимур 09.01.2022. Изменен вызов звуков
"""


class Player:
    def __init__(self, x, y, weapons, sprites, stats):
        self._x, self._y = x, y
        self.shot = False
        self.current_gun_index = 0
        self.weapons: list[Weapon] = weapons
        self.health = PLAYER_HEALTH
        self.direction = 0
        self.sprites = sprites
        self._stats = stats

    @property
    def pos(self) -> Point:
        return Point(self._x, self._y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def update(self):
        self._process_mouse()
        self._process_keyboard()
        self._play_sound()

    def damage(self, val=1):
        self.health -= val

    def dead(self):
        self.health = 0
        SpritesSound.dead(3)

    def draw(self):
        self._shot()

    def current_weapon(self):
        return self.weapons[self.current_gun_index]

    def set_weapon(self, delta):
        self._set_shot(False)
        self.weapons[self.current_gun_index].reset()
        GunSound.stop_sound()
        if delta == -1:
            if self.current_gun_index < 0:
                self.current_gun_index = 2
        self.current_gun_index -= delta
        self.current_gun_index %= len(self.weapons)

    def on_mouse_down(self, event):
        if event.button == pygame.BUTTON_LEFT:
            self.do_shot()
        if event.button == pygame.BUTTON_WHEELDOWN:
            self.set_weapon(-1)
        if event.button == pygame.BUTTON_WHEELUP:
            self.set_weapon(1)

    def shot_with_effects(self):
        Weapon.fire_sound(self.weapons[self.current_gun_index])
        self._set_shot(True)
        self.weapons[self.current_gun_index].shot()

    def do_shot(self):
        if self._can_shot():
            self.shot_with_effects()
            all_casted_sprites = sprites_ray_casting(self.sprites, self.pos, self.direction)
            ray_cast = Ray(self.pos, self.direction, MAX_VIEW_DISTANCE).ray_cast()
            ray_cast_distance = ray_cast.distance
            for sprite_hit in all_casted_sprites:
                sprite = self.sprites[sprite_hit.sprite_index]
                if self._is_can_kill_the_sprite(sprite_hit.angel, sprite_hit.distance,
                                                ray_cast_distance) and not sprite.is_dead:
                    self.sprites[sprite_hit.sprite_index].get_damage(self.current_weapon().damage)
                    SpritesSound.sprite_hit(3)
                    if isinstance(self.sprites[sprite_hit.sprite_index], MovableSprite):
                        self._stats.update_kills()
                    break
            else:
                SpritesSound.wall_hit(4)

        current_weapon = self.weapons[self.current_gun_index]
        if current_weapon.ammo <= 0:
            SpritesSound.no_ammo(3)

    @staticmethod
    def _is_hit_to_wall(sprite_hit_distance, distance_to_wall):
        return distance_to_wall <= sprite_hit_distance

    @staticmethod
    def _is_hooked_to_sprite(angel):
        return -SHOOTING_SPREAD <= int(math.degrees(angel)) <= SHOOTING_SPREAD

    @staticmethod
    def _is_can_hit_sprite(distance_to_sprite, distance_to_wall):
        return distance_to_sprite < distance_to_wall

    def _is_can_kill_the_sprite(self, angel, distance_to_sprite, distance_to_wall):
        return self._is_hooked_to_sprite(angel) and self._is_can_hit_sprite(distance_to_sprite, distance_to_wall)

    def _can_shot(self):
        current_weapon = self.weapons[self.current_gun_index]
        return not self.shot and current_weapon.ammo > 0

    def _set_shot(self, val):
        if (not val) == self.shot:
            self.shot = val

    def _process_keyboard(self):
        pressed_keys = pygame.key.get_pressed()
        cos_a, sin_a = math.cos(self.direction), math.sin(self.direction)
        if pressed_keys[pygame.K_w]:
            if self._can_move_forward():
                self._move_forward(cos_a, sin_a)
        if pressed_keys[pygame.K_s]:
            if self._can_move_backward():
                self._move_backward(cos_a, sin_a)
        if pressed_keys[pygame.K_a]:
            if self._can_move(self.direction - math.pi / 2, PLAYER_SIZE * 3):
                self._move_right(cos_a, sin_a)
        if pressed_keys[pygame.K_d]:
            if self._can_move(self.direction + math.pi / 2, PLAYER_SIZE * 3):
                self._move_left(cos_a, sin_a)

    def _can_move_forward(self):
        if self._can_move(self.direction, PLAYER_SIZE * 4):
            delta_angel = math.pi / 6
            if self._can_move(self.direction - delta_angel, PLAYER_SIZE * 4) and self._can_move(
                    self.direction + delta_angel, PLAYER_SIZE * 4):
                return True

        return False

    def _can_move_backward(self):
        if self._can_move(self.direction - math.pi, PLAYER_SIZE * 4):
            delta_angel = math.pi / 6 - math.pi
            if self._can_move(self.direction - delta_angel, PLAYER_SIZE * 4) and self._can_move(
                    self.direction + delta_angel, PLAYER_SIZE * 4):
                return True

        return False

    def _move_forward(self, cos_a, sin_a):
        self._x += cos_a * PLAYER_SPEED
        self._y += sin_a * PLAYER_SPEED

    def _move_backward(self, cos_a, sin_a):
        self._x += -cos_a * PLAYER_SPEED
        self._y += -sin_a * PLAYER_SPEED

    def _move_right(self, cos_a, sin_a):
        self._x += sin_a * PLAYER_SPEED
        self._y += -cos_a * PLAYER_SPEED

    def _move_left(self, cos_a, sin_a):
        self._x += -sin_a * PLAYER_SPEED
        self._y += cos_a * PLAYER_SPEED

    def _process_mouse(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_SCREEN_WIDTH
            pygame.mouse.set_pos((HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT))
            self.direction += difference * SENSITIVITY
            self.direction %= math.pi * 2

    def _shot(self):
        current_weapon = self.weapons[self.current_gun_index]
        if self.shot:
            self.shot = current_weapon.animation()
        else:
            current_weapon.static_animation()

    def _can_move(self, direction, collision_distance):
        ray = Ray(self.pos, direction, MAX_VIEW_DISTANCE)

        if ray.ray_cast().distance <= collision_distance:
            return False

        return True

    def _play_sound(self):
        pressed_keys = pygame.key.get_pressed()

        if (pressed_keys[pygame.K_w] or pressed_keys[pygame.K_s]
                or pressed_keys[pygame.K_a] or pressed_keys[pygame.K_d]):
            SpritesSound.footstep(1)
