import pygame


class Window:
    def __init__(self, title: str = 'Title', width: int = 900, height: int = 700):
        pygame.init()

        pygame.display.set_caption(title)

        self.display = pygame.display.set_mode((width, height), pygame.RESIZABLE)
