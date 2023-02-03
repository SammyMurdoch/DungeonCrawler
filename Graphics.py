import pygame
from Player import Player
from Level import Level
import numpy as np

class Graphics:
    def __init__(self, tile_matrix):
        self.tile_matrix = tile_matrix

    def move_object(self, current_position, direction):  # TODO is this the right class to put this in? Perhaps have a movable object class which monster, player inherit from
        moved_position = (current_position[0] + direction[0], current_position[1] + direction[1])

        if (moved_position[0] < 0) or (moved_position[0] >= len(self.tile_matrix[0])):
            return current_position
        elif (moved_position[1] < 0) or (moved_position[1] >= len(self.tile_matrix)):
            return current_position

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

            r_l = (player.coords[0] // columns) * columns
            r_u = r_l + columns + 1
            c_l = (player.coords[1] // rows) * rows
            c_u = c_l + rows + 1

            print(self.tile_matrix[r_l: r_u, c_l: c_u])

            for i, row in enumerate(self.tile_matrix[c_l: c_u, r_l: r_u]):  # TODO make a function for displaying each object type, potentially in their own classes
                for j, col in enumerate(row):
                    if col:
                        tile_rect.topleft = (j*square_size, i*square_size)
                        dungeon_surf.blit(tile_surf, tile_rect)

            player_centre_x = ((player.coords[0] % columns) + 1/2) * square_size
            player_centre_y = ((player.coords[1] % rows) + 1/2) * square_size

            player_rect.center = (player_centre_x, player_centre_y)
            dungeon_surf.blit(player_surf, player_rect)

            pygame.display.update()
#
tiles1 = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                   [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
                   [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0],
                   [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0],
                   [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

tiles2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                   [0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0],
                   [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                   [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                   [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])


tiles = np.concatenate((tiles1, tiles2), axis=1)

dungeon = Graphics(tiles)

dungeon.display_graphics()