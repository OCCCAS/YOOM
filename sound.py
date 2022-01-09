import random

import pygame

from config import MUSIC_FILES

"""
Батталов Арслан 05.01.2022 Добавлен класс Music и SoundEffect
Батталов Арслан 07.01.2022. Добавлен класс GunSound
Батталов Арслан 08.01.2022. Добавлен класс MenuMusic
08.01.2022. Добавлено выключение и включение звуков
"""


class Music:
    def __init__(self, path=MUSIC_FILES):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        self.path = path
        self.theme = pygame.mixer.music
        self.init_track()

    def init_track(self):
        random.shuffle(self.path)
        self.theme.load(self.path.pop(0))
        for file in self.path:
            self.theme.queue(file)

    def play_music(self):
        if self.theme.get_volume() != 0:
            self.theme.set_volume(0.1)
            self.theme.play()

    def change_music_volume(self, volume):
        self.theme.set_volume(volume)


class MenuMusic(Music):
    def __init__(self, path):
        super().__init__(path)
        self.path = path

    def init_track(self):
        self.theme.load(self.path)


class SoundEffect:
    def __init__(self, path):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        self.init_track(path)

    def init_track(self, path):
        self.effect = pygame.mixer.Sound(path)

    def play_sound(self):
        if not pygame.mixer.Channel(2).get_busy():
            pygame.mixer.Channel(2).play(self.effect)
    @staticmethod
    def change_effects_volume(volume):
        pygame.mixer.Channel(2).set_volume(volume)
        pygame.mixer.Channel(1).set_volume(volume)


class GunSound(SoundEffect):
    def play_sound(self):
        pygame.mixer.Channel(1).play(self.effect)

    @staticmethod
    def stop_sound():
        pygame.mixer.Channel(1).stop()
