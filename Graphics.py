import pygame
from Player import Player

class Graphics:
    def __init__(self, display_tiles):
        self.display_tiles = display_tiles

    def display_graphics(self):
        pygame.init()
        window_size = (700, 700)
        dungeon_surf = pygame.display.set_mode(window_size)

        player = Player(None, None, None, [35, 35], pygame.image.load("Player.png").convert_alpha())

        player_surf = player.texture
        player_rect = player_surf.get_rect()
        player_rect.center = player.coords

        rows = 10
        columns = 10
        square_size = window_size[0] // rows

        up_key = 273
        down_key = 274
        right_key = 275
        left_key = 276

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    print("yes")
                    if event.key == pygame.K_UP:
                        player.coords[1] -= 70
                    elif event.key == pygame.K_DOWN:
                        player.coords[1] += 70
                    elif event.key == pygame.K_RIGHT:
                        player.coords[0] += 70
                    elif event.key == pygame.K_LEFT:
                        player.coords[0] -= 70

                    print(player.coords)

            dungeon_surf.fill((0, 0, 0))

            player_rect.center = player.coords

            for row in range(rows):
                for col in range(columns):
                    if (row, col) in self.display_tiles:
                        if (row+col) % 2:
                            colour = (100, 0, 0)
                        else:
                            colour = (200, 100, 0)

                        square = pygame.Rect(col * square_size, row * square_size, square_size, square_size)
                        pygame.draw.rect(dungeon_surf, colour, square)

                        dungeon_surf.blit(player_surf, player_rect)

            pygame.display.update()


hi = Graphics([(0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (4, 5)])

hi.display_graphics()

# piece_rects[board[node][0][0]].center = board[node][2]
# screen.blit(piece_surfs[board[node][0][0]], piece_rects[board[node][0][0]])
# 
# piece_surfs = {piece_type[0]: pygame.image.load(piece_type[2]).convert_alpha() for piece_type in piece_data.keys()}
# piece_rects = {piece_type: piece_surfs[piece_type].get_rect() for piece_type in piece_surfs.keys()}
