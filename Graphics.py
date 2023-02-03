import pygame
from Player import Player

class Graphics:
    def __init__(self, display_tiles):
        self.display_tiles = display_tiles

    def move_object(self, current_position, direction):  # TODO is this the right class to put this in?
        moved_position = (current_position[0] + direction[0], current_position[1] + direction[1])
        if moved_position in self.display_tiles:
            return moved_position
        else:
            return current_position

    def display_graphics(self):
        pygame.init()

        dungeon_surf = pygame.display.set_mode((3840, 2400), pygame.FULLSCREEN)

        rows = 10
        columns = int((rows/5)*8)  # TODO not used but could be needed to set bounds on coordinates

        square_size = dungeon_surf.get_height()//rows

        player = Player(None, None, None, (0, 0), pygame.image.load("Player.png").convert_alpha())

        player_surf = player.texture
        player_rect = player_surf.get_rect()
        player_rect.center = player.coords

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        player.coords = Graphics.move_object(self, player.coords, [0, -1])
                    elif event.key == pygame.K_DOWN:
                        player.coords = Graphics.move_object(self, player.coords, [0, 1])
                    elif event.key == pygame.K_RIGHT:
                        player.coords = Graphics.move_object(self, player.coords, [1, 0])
                    elif event.key == pygame.K_LEFT:
                        player.coords = Graphics.move_object(self, player.coords, [-1, 0])

            dungeon_surf.fill((128, 128, 128))

            for tile in self.display_tiles:  # TODO make a function for displaying each object type, potentially in their own classes
                tile_surf = pygame.image.load("tile_hatch.png").convert_alpha()
                tile_rect = tile_surf.get_rect()
                tile_rect.topleft = (tile[0]*square_size, tile[1]*square_size)
                dungeon_surf.blit(tile_surf, tile_rect)

            player_rect.center = ((player.coords[0] + 1/2) * square_size, (player.coords[1] + 1/2) * square_size)  # TODO make this a function
            dungeon_surf.blit(player_surf, player_rect)

            pygame.display.update()

hi = Graphics([(0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (2, 5), (3, 5), (4, 5), (2, 2), (3, 2), (4, 2),
               (4, 3), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (9, 5), (9, 6), (10, 6), (11, 6), (12, 6),
               (13, 6), (13, 7), (13, 8), (12, 7), (12, 8), (14, 8), (15, 8), (11, 4), (12, 4), (12, 5)])

hi.display_graphics()

