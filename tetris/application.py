from .board import Board
from .input_handler import InputHandler
from .window import Window


class Application:
    def __init__(self):
        self.window = Window(title='Tetris', width=1280, height=1000)
        self.input_handler = InputHandler(app=self)
        self.new_board()
        self.main()

    def main(self):
        self.running = True

        while self.running:
            self.board.think()
            self.input_handler.think()

    def new_board(self):
        self.board = Board(display=self.window.display)
