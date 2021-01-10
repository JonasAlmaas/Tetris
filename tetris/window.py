import pygame
from pathlib import Path


class Window:
    def __init__(self, title: str = 'Title', width: int = 900, height: int = 700):
        pygame.init()

        icon = pygame.image.load(str(Path(__file__).parent / 'images/icon.png'))

        pygame.display.set_caption(title)
        pygame.display.set_icon(icon)

        self.display = pygame.display.set_mode((width, height), pygame.RESIZABLE)
