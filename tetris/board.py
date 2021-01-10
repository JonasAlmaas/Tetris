import pygame
import numpy as np

from .piece import Piece
from .block import Block


class Board:
    def __init__(self, display=None, rows: int = 20, cols: int = 10, margin_board: int = 30, margin_block: int = 1):
        self.display = display
        self.game_running = True

        self._score = 0
        self.font_score = pygame.font.SysFont(None, 50)
        self.font_game_over = pygame.font.SysFont(None, 72)

        self.rows = rows
        self.cols = cols

        self._margin_board = margin_board
        self._margin_block = margin_block

        self._bg_color = pygame.Color('#303030')

        self.matrix = []
        for row in range(self.rows):
            self.matrix.append([])
            for _ in range(self.cols):
                self.matrix[row].append(Block(type='empty'))

        self.new_piece()

    def think(self):
        self.draw()

        if self.game_running:
            self.active_piece.move_down()

    def next_round(self):
        self.active_piece.place(self.matrix)

        self.new_piece()

        self.check_for_full_row()

        for col in range(self.cols):
            if self.matrix[0][col].type != 'empty':
                self.game_running = False
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

        board_height = self.display.get_size()[1] - self._margin_board * 3
        board_width = board_height / self.rows * self.cols

        board_x = self.display.get_size()[0] / 2 - board_width / 2
        board_y = self._margin_board * 2

        pygame.draw.rect(self.display, self._bg_color,(board_x, board_y, board_width + self._margin_block, board_height + self._margin_block))

        score = self.font_score.render(str(self._score), True, pygame.Color('#ffffff'))
        score_pos = self.display.get_size()[0] // 2 - score.get_rect().width // 2, self._margin_board - score.get_rect().height // 2
        self.display.blit(score, score_pos)

        temp_matrix = np.copy(self.matrix)
        self.active_piece.place_gost(matrix=temp_matrix)
        self.active_piece.place(matrix=temp_matrix)

        block_size = board_width / self.cols - self._margin_block

        for row in range(self.rows):
            for col in range(self.cols):
                block_x = col * (board_width / self.cols) + board_x + self._margin_block
                block_y = row * (board_width / self.cols) + board_y + self._margin_block

                color = temp_matrix[row][col].color
                pygame.draw.rect(self.display, color,(block_x, block_y, block_size, block_size))

        if not self.game_running:
            self.draw_game_over()

        pygame.display.update()

    def draw_game_over(self):
        board_height = self.display.get_size()[1] - self._margin_board * 3
        board_width = board_height / self.rows * self.cols

        board_x = self.display.get_size()[0] / 2 - board_width / 2
        board_y = self._margin_board * 2

        board = pygame.Surface((board_width, board_height))
        board.set_alpha(200)
        board.fill(self._bg_color)
        self.display.blit(board, (board_x, board_y))

        game_over = self.font_game_over.render('GAME OVER', True, pygame.Color('#ffffff'))
        game_over_pos = self.display.get_size()[0] // 2 - game_over.get_rect().width // 2, self.display.get_size()[1] // 2 - game_over.get_rect().height // 2
        self.display.blit(game_over, game_over_pos)

    def new_piece(self):
        self.active_piece = Piece(board=self)
