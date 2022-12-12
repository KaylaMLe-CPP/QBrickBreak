import pygame

from assets.circuit_grid import CircuitGrid
from assets import globals

pygame.init()
screen = pygame.display.set_mode((1200, 750))
pygame.display.set_caption('QPong')
clock = pygame.time.Clock()

def main():
    # initialize game
    circuit_grid = CircuitGrid(5, globals.FIELD_HEIGHT)
    exit = False
    
    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
                
        # update game
        
        #draw game
        circuit_grid.draw(screen)
        pygame.display.flip()
        
        # 60 fps
        clock.tick(60)
        
if __name__ == '__main__':
    main()