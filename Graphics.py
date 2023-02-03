import pygame
from Player import Player
from Level import Level
import numpy as np

class Graphics:
    # def __init__(self, display_tiles):
    #     self.display_tiles = display_tiles

    def __init__(self, tile_matrix):
        self.tile_matrix = tile_matrix

    def move_object(self, current_position, direction):  # TODO is this the right class to put this in? Perhaps have a movable object class which monster, player inherit from
        moved_position = (current_position[0] + direction[0], current_position[1] + direction[1])
        if self.tile_matrix[moved_position[1], moved_position[0]]:
            return moved_position
        else:
            return current_position

    #def generate_tile_position(self, tiles):



    def display_graphics(self):  # TODO once you reach the edge of the screen display the next set of tiles
        pygame.init()

        dungeon_surf = pygame.display.set_mode((3840, 2400), pygame.FULLSCREEN)

        rows = 10
        columns = int((rows/5)*8)  # TODO not used but could be needed to set bounds on coordinates

        square_size = dungeon_surf.get_height()//rows

        player = Player(None, None, None, (0, 0), pygame.image.load("Player.png").convert_alpha())

        player_surf = player.texture
        player_rect = player_surf.get_rect()
        player_rect.center = player.coords

        tile_surf = pygame.image.load("tile_hatch.png").convert_alpha()
        tile_rect = tile_surf.get_rect()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player.coords = Graphics.move_object(self, player.coords, [0, -1])
                    elif event.key == pygame.K_DOWN:
                        player.coords = Graphics.move_object(self, player.coords, [0, 1])
                    elif event.key == pygame.K_RIGHT:
                        player.coords = Graphics.move_object(self, player.coords, [1, 0])
                    elif event.key == pygame.K_LEFT:
                        player.coords = Graphics.move_object(self, player.coords, [-1, 0])
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

            dungeon_surf.fill((128, 128, 128))

            for i, row in enumerate(self.tile_matrix):  # TODO make a function for displaying each object type, potentially in their own classes
                for j, col in enumerate(row):
                    if col:
                        tile_rect.topleft = (j*square_size, i*square_size)
                        dungeon_surf.blit(tile_surf, tile_rect)

            player_rect.center = ((player.coords[0] + 1/2) * square_size, (player.coords[1] + 1/2) * square_size)  # TODO make this a function
            dungeon_surf.blit(player_surf, player_rect)

            pygame.display.update()

tiles = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                  [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0],
                  [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

dungeon = Graphics(tiles)

dungeon.display_graphics()

