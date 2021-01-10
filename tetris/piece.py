import random
import copy

from .block import Block


types = {
        'i': [[-1, 0], [0, 0] ,[1, 0], [2, 0]],
        'j': [[-1, 0], [0, 0], [1, 0], [1, -1]],
        'l': [[-1, 0], [0, 0], [1, 0], [1, 1]],
        'o': [[-1, 0], [-1, -1], [0, 0], [0, -1]],
        't': [[0, -1], [0, 0], [0, 1], [1, 0]],
        'z': [[0, -1], [0, 0], [1, 0], [1, 1]],
        's': [[-1, 0], [0, 0], [0, -1], [-1, 1]]
        }


class Piece:
    def __init__(self, board):
        self._board = board
        self._pos = [-1, self._board.cols // 2]
        self._type = random.choice(list(types.keys()))
        self._coords = types[self._type]

        for _ in range(random.randrange(3, -1, -1)):
            self.rotate()

    def place(self, matrix):
        for coord in self._coords:
            row_global, col_global = self.get_global_coord(coord,  self._pos)

            if 0 <= row_global < self._board.rows and 0 <= col_global < self._board.cols:
                matrix[row_global][col_global] = Block(type=self._type)

    def place_gost(self, matrix):
        temp_coords = copy.deepcopy(self._coords)
        temp_pos = copy.deepcopy(self._pos)

        is_down = False

        while not is_down:
            for coord in temp_coords:
                row = coord[0] + temp_pos[0]
                col = coord[1] + temp_pos[1]

                if self._board.is_empty_coord((row + 1, col)):
                    continue

                is_down = True

            if is_down:
                break

            temp_pos[0] += 1

        for coord in temp_coords:
            row = coord[0] + temp_pos[0]
            col = coord[1] + temp_pos[1]
            
            if row >= 0:
                matrix[row][col] = Block(type='gost')

    def get_global_coord(self, coord, pos):
        row = coord[0] + pos[0]
        col = coord[1] + pos[1]

        return (row, col)

    def move_down(self):
        if not self._board.game_running:
            return

        for coord in self._coords:
            row, col = self.get_global_coord(coord,  self._pos)

            if self._board.is_empty_coord((row + 1, col)):
                continue

            self._board.next_round()
            return True

        self._pos[0] += 1

    def hard_drop(self):
        if not self._board.game_running:
            return

        while True:
            if self.move_down():
                return

            self._board.draw()

    def move_right(self):
        if not self._board.game_running:
            return

        for coord in self._coords:
            row, col = self.get_global_coord(coord,  self._pos)

            if self._board.is_empty_coord((row, col + 1)):
                continue

            return

        self._pos[1] += 1

    def move_left(self):
        if not self._board.game_running:
            return

        for coord in self._coords:
            row, col = self.get_global_coord(coord,  self._pos)

            if self._board.is_empty_coord((row, col - 1)):
                continue

            return
        self._pos[1] -= 1

    def rotate(self):
        if not self._board.game_running:
            return

        if self._type == 'o':
            return

        new_coords = copy.deepcopy(self._coords)
        temp_pos = copy.deepcopy(self._pos)
        
        loops = 0
        moves = 0

        while not self.can_rotate(new_coords, temp_pos)[0]:
            direction = self.can_rotate(new_coords, temp_pos)[1]

            loops += 1

            if direction > 0:
                moves -= 1
                temp_pos[1] -= 1

            elif direction < 0:
                moves += 1
                temp_pos[1] += 1

            if loops > 5:
                return

        if moves > 0:
            for _ in range(moves):
                self.move_right()

        elif moves < 0:
            for _ in range(abs(moves)):
                self.move_left()
    
        for coord in new_coords:
            coord.reverse()
            coord[0] = -coord[0]

            coord = self.get_global_coord(coord, self._pos)

            if not self._board.is_empty_coord(coord):
                return

        self._coords = new_coords

    def can_rotate(self, coords, pos):
        coords = copy.deepcopy(coords)

        for coord in coords:
            coord.reverse()
            coord[0] = -coord[0]

            coord = self.get_global_coord(coord, pos)

            direction = coord[1] - pos[1]

            if not self._board.is_empty_coord(coord):
                return False, direction

        return True, None
