import time

from .window import Window
from .board import Board
from .input_handler import InputHandler


class Application:
    def __init__(self):
        self.tick_rate = 2
        self.last_update = 0

        self.window = Window(title='Tetris', width=1280, height=1000)
        self.input_handler = InputHandler(app=self)
        self.new_board()

        self.loop()

    def loop(self):
        self.running = True

        while self.running:
            if time.time() - self.last_update > 1 / self.tick_rate:
                self.reset_update_time()
                self.board.think()

            self.input_handler.think()

    def reset_update_time(self):
        self.last_update = time.time()

    def new_board(self):
        self.board = Board(display=self.window.display)

    def reset(self):
        self.reset_update_time()
        self.new_board()
