import pygame


class InputHandler:
    def __init__(self, app):
        self.app = app

    def think(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.app.reset()

                elif event.key == pygame.K_SPACE:
                    self.app.reset_update_time()
                    self.app.board.active_piece.hard_drop()
                    self.app.board.draw()

                elif event.key == pygame.K_DOWN:
                    self.app.reset_update_time()
                    self.app.board.active_piece.move_down()
                    self.app.board.draw()
                
                elif event.key == pygame.K_LEFT:
                    self.app.board.active_piece.move_left()
                    self.app.board.draw()

                elif event.key == pygame.K_RIGHT:
                    self.app.board.active_piece.move_right()
                    self.app.board.draw()

                elif event.key == pygame.K_z:
                    self.app.board.active_piece.rotate()
                    self.app.board.draw()
