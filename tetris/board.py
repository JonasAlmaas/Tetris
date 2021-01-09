import pygame
import numpy as np

from .piece import Piece
from .block import Block


class Board:
    def __init__(self, display=None, rows: int = 20, cols: int = 10, margin_board: int = 30, margin_block: int = 1):
        self.display = display
        self.game_running = True

        self._score = 0
        self.font = pygame.font.SysFont(None, 50)

        self.rows = rows
        self.cols = cols

        self._margin_board = margin_board
        self._margin_block = margin_block

        self._bg_color = pygame.Color('#303030')
        self.new_piece_pos = [-1, self.cols // 2]

        self.matrix = []
        for row in range(self.rows):
            self.matrix.append([])
            for _ in range(self.cols):
                self.matrix[row].append(Block(type='empty'))

        self.new_piece()

    def think(self):
        if self.game_running:
            self.active_piece.move_down()
            self.draw()

    def next_round(self):
        self.active_piece.place(self.matrix)

        self.new_piece()

        self.check_for_full_row()

        for col in range(self.cols):
            if self.matrix[0][col].type != 'empty':
                self.game_running = False
                print('Game Over')
                return

    def check_for_full_row(self):
        full_rows = 0

        for row in range(self.rows):
            is_full_row = True
            for col in range(self.cols):
                if self.matrix[row][col].type == 'empty':
                    is_full_row = False

            if is_full_row:
                self.remove_row(row)
                full_rows += 1

        if full_rows != 4:
            self._score += full_rows * 100
        else:
            self._score += full_rows * 100 * 2

    def remove_row(self, row):
        for col in range(self.cols):
            self.matrix[row][col].set_type('empty')
            self.draw()

        for r in reversed(range(0, row + 1)):
            for col in range(self.cols):
                if r - 1 >= 0:
                    self.matrix[r][col] = self.matrix[r - 1][col]

            self.draw()

    def is_empty_coord(self, coord):
        row, col = coord

        try:
            if row < 0:
                return True
            
            if col < 0:
                return False

            if self.matrix[row][col].type == 'empty':
                return True
        except:
            return False

    def draw(self):
        self.display.fill(pygame.Color('#454545'))

        height = self.display.get_size()[1] - self._margin_board * 3
        width = height / self.rows * self.cols
        pos_x = self.display.get_size()[0] / 2 - width / 2
        pos_y = self._margin_board * 2
        pygame.draw.rect(self.display, self._bg_color,(pos_x, pos_y, width + self._margin_block, height + self._margin_block))

        score = self.font.render(str(self._score), True, pygame.Color('#ffffff'))
        score_pos = self.display.get_size()[0] // 2 - score.get_rect().width // 2, self._margin_board - score.get_rect().height // 2
        self.display.blit(score, score_pos)

        temp_matrix = np.copy(self.matrix)
        self.active_piece.place_gost(matrix=temp_matrix)
        self.active_piece.place(matrix=temp_matrix)

        block_size = width / self.cols - self._margin_block

        for row in range(self.rows):
            for col in range(self.cols):
                block_x = col * (width / self.cols) + pos_x + self._margin_block
                block_y = row * (width / self.cols) + pos_y + self._margin_block

                color = temp_matrix[row][col].color
                pygame.draw.rect(self.display, color,(block_x, block_y, block_size, block_size))

        pygame.display.update()

    def new_piece(self):
        self.active_piece = Piece(board=self)
