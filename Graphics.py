import pygame
from Player import Player

class Graphics:
    def __init__(self, display_tiles):
        self.display_tiles = display_tiles

    def display_graphics(self):
        pygame.init()

        dungeon_surf = pygame.display.set_mode((3840, 2400), pygame.FULLSCREEN)

        rows = 10
        columns = int((rows/5)*8)

        square_size = dungeon_surf.get_height()//rows

        player = Player(None, None, None, [0, 0], pygame.image.load("Player.png").convert_alpha())

        player_surf = player.texture
        player_rect = player_surf.get_rect()
        player_rect.center = player.coords

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:  # TODO make the coordinate of the square change not the pixel to be able to detect wall collisions
                    if event.key == pygame.K_UP:  # TODO make this less code
                        if (player.coords[0], player.coords[1] - 1) in self.display_tiles:
                            player.coords[1] -= 1
                    elif event.key == pygame.K_DOWN:
                        if (player.coords[0], player.coords[1] + 1) in self.display_tiles:
                            player.coords[1] += 1
                    elif event.key == pygame.K_RIGHT:
                        if (player.coords[0] + 1, player.coords[1]) in self.display_tiles:
                            player.coords[0] += 1
                    elif event.key == pygame.K_LEFT:
                        if (player.coords[0] - 1, player.coords[1]) in self.display_tiles:
                            player.coords[0] -= 1

            dungeon_surf.fill((0, 0, 0))


            player_rect.center = ((player.coords[0] + 1/2) * square_size, (player.coords[1] + 1/2) * square_size)  # TODO make this a function
            for row in range(rows):
                for col in range(columns):
                    if (row, col) in self.display_tiles:
                        if (row+col) % 2:
                            colour = (100, 0, 0)
                        else:
                            colour = (200, 100, 0)

                        square = pygame.Rect(row * square_size, col * square_size, square_size, square_size)
                        pygame.draw.rect(dungeon_surf, colour, square)

            dungeon_surf.blit(player_surf, player_rect)

            pygame.display.update()

hi = Graphics([(0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (1, 4), (2, 4), (2, 5), (3, 5), (4, 5), (2, 2), (3, 2), (4, 2),
               (4, 3), (4, 4)])

hi.display_graphics()

