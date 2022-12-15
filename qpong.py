import pygame

from assets.circuit_grid import CircuitGrid
from assets import globals, ui, paddle, ball, computer, brick

pygame.init()
screen = pygame.display.set_mode((1200, 750))
pygame.display.set_caption('QPong')
clock = pygame.time.Clock()


def main():
    # initialize game

    # left edge + margin
    classical_paddle = paddle.Paddle(9 * globals.WIDTH_UNIT)
    # right edge - margin
    quantum_paddles = paddle.QuantumPaddles(
        globals.WINDOW_WIDTH - 9 * globals.WIDTH_UNIT)
    quantum_bricks = brick.Qubricks(
        globals.WINDOW_WIDTH // 2 - (globals.PADDLE_HEIGHT // 2))

    circuit_grid = CircuitGrid(5, globals.FIELD_HEIGHT)
    pong_ball = ball.Ball()
    classical_computer = computer.ClassicalComputer(classical_paddle)
    quantum_computer = computer.QuantumComputer(
        quantum_paddles, quantum_bricks, circuit_grid)

    moving_sprites = pygame.sprite.Group()
    moving_sprites.add(classical_paddle)
    moving_sprites.add(quantum_paddles.paddles)
    moving_sprites.add(pong_ball)
    moving_sprites.add(quantum_bricks.bricks)

    exit = False
    while not exit:
        # update game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
            elif event.type == pygame.KEYDOWN:
                circuit_grid.handle_input(event.key)

        pong_ball.update(classical_computer, quantum_computer)
        classical_computer.update(pong_ball)
        quantum_computer.update(pong_ball)

        # draw game
        screen.fill(globals.BLACK)  # erase current frame

        if classical_computer.score >= globals.WIN_SCORE:
            ui.draw_lose_scene(screen)
            exit = True

        elif quantum_computer.score >= globals.WIN_SCORE:
            ui.draw_win_scene(screen)
            exit = True

        else:
            circuit_grid.draw(screen)

            ui.draw_statevector_grid(screen)
            ui.draw_score(screen, classical_computer.score,
                          quantum_computer.score)
            ui.draw_dashed_line(screen)

            moving_sprites.draw(screen)

        pygame.display.flip()

        # 60 fps
        clock.tick(60)


if __name__ == '__main__':
    main()
