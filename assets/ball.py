# sprite file
import pygame
import random

from . import globals


class Ball(pygame.sprite.Sprite):
    # draws the ball
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([globals.WIDTH_UNIT, globals.WIDTH_UNIT])
        self.image.fill(globals.WHITE)
        self.rect = self.image.get_rect()

        self.velocity = [1, 2]  # initial movement direction
        self.initial_speed = 2
        self.reset(1)

    # moves the ball based on the velocity
    def update(self, classical_computer, quantum_computer):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # if top/bottom edge is detected, flip direction
        if self.rect.y < 0 or self.rect.y > globals.FIELD_HEIGHT - globals.WIDTH_UNIT:
            self.velocity[1] = -self.velocity[1]

        if self.rect.x < 0:
            self.reset(1)
            quantum_computer.score += 1

        elif self.rect.x > globals.WINDOW_WIDTH:
            self.reset(-1)
            classical_computer.score += 1

    def bounce(self):
        # reverse x and y velocity, increase speed
        self.velocity[0] = -self.velocity[0] * 1.5
        self.velocity[1] = -self.velocity[1] * 1.5

    def reset(self, direction):
        # the ball starts on the classical computer side
        self.rect.centerx = (globals.WINDOW_WIDTH / 2) - \
            (globals.PADDLE_HEIGHT)
        self.rect.centery = globals.FIELD_HEIGHT / 2

        if direction > 0:
            self.velocity = [random.randint(
                2, 4), random.randint(-4, 4)] * self.initial_speed
        else:
            self.velocity = [
                random.randint(-4, -2), random.randint(-4, 4)] * self.initial_speed
