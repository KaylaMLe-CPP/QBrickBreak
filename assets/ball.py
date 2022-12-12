# sprite file
import pygame

from . import globals


class Ball(pygame.sprite.Sprite):
    # draws the ball
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([globals.WIDTH_UNIT, globals.WIDTH_UNIT])
        self.image.fill(globals.WHITE)
        self.rect = self.image.get_rect()
        self.velocity = [1, 2]  # initial movement direction

    # moves the ball based on the velocity
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # if top/bottom edge is detected, flip direction
        if self.rect.y < 0 or self.rect.y > globals.FIELD_HEIGHT - globals.WIDTH_UNIT:
            self.velocity[1] = -self.velocity[1]
