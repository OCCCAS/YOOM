import pygame

from config import *
from map import create_map, create_minimap
from player import Player
from render import Render
from sound import Music
from sprite import create_sprites
from utils import is_game_over
from weapon import Weapon, GunSound
from menu import MainMenu, show_info, show_game_over

"""
Павлов Тимур 26.12.2021. Создан класс Game
Вайман Ангелина 28.12.2021. Внесены поправки
Вайман Ангелина 03.01.2022. Создана новая поверхность screen_map для миникарты
Батталов Арслан 05.01.2022. Добавлены функция play_theme
Батталов Арслан 08.01.2022 Добавлена поддержка звуков выстрела
Павлов Тимур 08.01.2022. Исправлена ошибка анимации оружия
Батталов Арслан 08.01.2022 Исправлена проблема двойного проигрывания звуков
"""


# level = load_level('level1.txt')


class Game:
    def __init__(self, caption=WINDOW_NAME):
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
        self.screen_map = pygame.Surface((MAP_SIZE[0] * MAP_TILE, MAP_SIZE[1] * MAP_TILE))
        self.clock = pygame.time.Clock()

        self.weapons = [
            Weapon(self.screen, 'Gun1', (500, 450), 12, SHOTGUN, 5),
            Weapon(self.screen, 'Gun2', (400, 400), 2, PISTOL, 25),
            Weapon(self.screen, 'Gun3', (350, 300), 10, RIFLE, 10)
        ]
        self.player = Player(TILE * 2 - TILE // 2, TILE * 2 - TILE // 2, self.weapons)
        self.sprites = create_sprites()
        self.render = Render(self.screen, self.player, self.screen_map, self.sprites)
        self.caption = caption
        self.menu = MainMenu(self.screen, self.clock)
        self._game_over = False

    def run(self):
        self.menu.run()
        self._init()
        # self.play_theme(THEME_MUSIC)
        self._config()
        self._update()
        self._finish()

    def _init(self):
        create_map(self.menu.chosen_level)
        create_minimap(self.menu.chosen_level)
        pygame.init()

    def _config(self):
        pygame.display.set_caption(self.caption)
        pygame.mouse.set_visible(False)

    def _update(self):
        running = True
        while running:
            self.screen.fill(SKYBLUE)
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                if self._game_over:
                    if event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        self.sprites = self.player.do_shot(self.sprites)
                    if event.button == pygame.BUTTON_WHEELDOWN:
                        self.player.set_weapon(-1)
                    if event.button == pygame.BUTTON_WHEELUP:
                        self.player.set_weapon(1)

            if not self._game_over:
                self.player.update()
                self.render.render()
                show_info(self.screen, self.player)

            if is_game_over(self.player, self.sprites):
                show_game_over(self.screen)
                self._game_over = True

            pygame.display.set_caption('FPS: ' + str(int(self.clock.get_fps())))
            pygame.display.flip()

    @staticmethod
    def _finish():
        pygame.quit()

    @staticmethod
    def play_theme(path):
        theme = Music(path)
        theme.play_music()


if __name__ == '__main__':
    game = Game()
    game.run()
