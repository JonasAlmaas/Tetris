import pygame
from pathlib import Path


class Music:
    def __init__(self):
        pygame.mixer.init()

        self._muted = False

        song_path = str(Path(__file__).parent / 'misc/tetris.mp3')
        self._sound = pygame.mixer.Sound(song_path)
        self.set_volume(0.15)

        self.play()

    def play(self):
        self._sound.play(9999)

    def stop(self):
        self._sound.stop()

    def set_volume(self, volume: float):
        self._volume = volume
        self._sound.set_volume(self._volume)
    
    def toggle_mute(self):
        if self._muted:
            self._muted = False
            self._sound.set_volume(self._volume)
        else:
            self._muted = True
            self._sound.set_volume(0)
