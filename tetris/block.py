import pygame


types = {
    'empty': pygame.Color('#363636'),
    'gost': pygame.Color('#424242'),
    't': pygame.Color('#c625f7'),
    'j': pygame.Color('#256ff7'),
    'z': pygame.Color('#f73325'),
    's': pygame.Color('#25f73a'),
    'o': pygame.Color('#f4f725'),
    'l': pygame.Color('#f7b825'),
    'i': pygame.Color('#25edf7')
}


class Block:
    def __init__(self, type: str = 'empty'):
        self.set_type(type=type)

    def set_type(self, type: str):
        self.type = type
        self.color = types[self.type]
