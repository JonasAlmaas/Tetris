from .input_handler import InputHandler
from .window import Window
from .board import Board
from .music import Music


class Application:
    def __init__(self):
        self.input_handler = InputHandler(app=self)
        self.window = Window(title='Tetris', width=1280, height=1000)
        self.music = Music()
        self.new_board()
        self.main()

    def main(self):
        self.running = True

        while self.running:
            self.board.think()
            self.input_handler.think()

    def new_board(self):
        self.board = Board(display=self.window.display)
