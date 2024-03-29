import pygame
from Player import Player
from Monster import Monster
import numpy as np
from Level import Level, level

#from DungeonGenerator import hi


class MatrixedObject:  # TODO inherit from dungeon which has dungeon_surf and grid_spacing
    def __init__(self, matrix, texture_path, grid_spacing, rotation=0):
        self.matrix = matrix
        self.surf = pygame.image.load(texture_path).convert_alpha()  # TODO for testing reasons, don't have this in a function
        self.surf = pygame.transform.rotate(self.surf, rotation)
        self.rect = self.surf.get_rect()
        self.grid_spacing = grid_spacing

    def display(self, display_surf, cols, rows):
        for i, row in enumerate(self.matrix[rows[0]: rows[1], cols[0]: cols[1]]):
            for j, col in enumerate(row):
                if col:
                    self.rect.topleft = (j * self.grid_spacing, i * self.grid_spacing)
                    display_surf.blit(self.surf, self.rect)


class Walls(MatrixedObject):
    def __init__(self, tile_matrix: np.ndarray, position: str, grid_spacing, rows: int, cols: int):
        self.position = position
        matrix = Walls.create_wall_matrix(tile_matrix, self.position, rows, cols)
        wall_data = {"top": {"texture": "wall.png", "rotation": 0},
                    "right": {"texture": "wall.png", "rotation": 270},
                    "bottom": {"texture": "wall.png", "rotation": 180},
                    "left": {"texture": "wall.png", "rotation": 90}}

        MatrixedObject.__init__(self, matrix, wall_data[position]["texture"], grid_spacing, rotation=wall_data[position]["rotation"])

    @staticmethod
    def mirror_vertically(matrix: np.ndarray) -> np.ndarray:
        return matrix[::-1]

    @staticmethod
    def transpose(matrix: np.ndarray) -> np.ndarray:
        return matrix.transpose()

    @staticmethod
    def create_wall_matrix(tile_matrix: np.ndarray, position: str, screen_rows: int, screen_cols: int) -> np.ndarray: # TODO split this up
        """Create a matrix for the walls in a given rotation."""
        if position in ['top', 'bottom']:
            wall_matrix = np.zeros(tile_matrix.shape)
            extra_wall_frequency = screen_rows
        else:
            wall_matrix = np.zeros(tile_matrix.shape[::-1])
            extra_wall_frequency = screen_cols

        pipelines = {'top': [],
         'bottom': [Walls.mirror_vertically],
         'left': [Walls.transpose],
         'right': [Walls.transpose, Walls.mirror_vertically]
         }

        template_matrix = tile_matrix
        for transform in pipelines[position]:
            template_matrix = transform(template_matrix)

        for i in range(len(wall_matrix)):
            on_screen_edge = not i % extra_wall_frequency
            on_tile_matrix_edge = i

            if on_screen_edge:
                if on_tile_matrix_edge:
                    wall_matrix[i] = template_matrix[i] - template_matrix[i - 1]
                else:
                    wall_matrix[i] = template_matrix[i]
            else:
                wall_matrix[i] = template_matrix[i - 1] - template_matrix[i]

        wall_matrix[wall_matrix < 0] = 0

        for transform in pipelines[position][::-1]:
            wall_matrix = transform(wall_matrix)

        return wall_matrix

    # def create_corner_wall_matrix(self):


class Dungeon:
    def __init__(self):
        self.surf = pygame.display.set_mode((3840, 2400), pygame.FULLSCREEN)
        self.rows = 10 #  TODO changing this doesn't work as the tile/player can't be scaled
        self.columns = int((self.rows/5)*8)
        self.square_size = self.surf.get_height() // self.rows


class Graphics:
    def __init__(self, tile_matrix: np.ndarray, player_position):
        self.dungeon = Dungeon()

        self.tiles = MatrixedObject(tile_matrix, "tile_hatch.png", self.dungeon.square_size)

        self.walls_top = Walls(tile_matrix, "top", self.dungeon.square_size, self.dungeon.rows, self.dungeon.columns)
        self.walls_bottom = Walls(tile_matrix, "bottom", self.dungeon.square_size, self.dungeon.rows, self.dungeon.columns)
        self.walls_right = Walls(tile_matrix, "right", self.dungeon.square_size, self.dungeon.rows, self.dungeon.columns)
        self.walls_left = Walls(tile_matrix, "left", self.dungeon.square_size, self.dungeon.rows, self.dungeon.columns)


    def move_object(self, current_position, direction):  # TODO is this the right class to put this in? Perhaps have a movable object class which monster, player inherit from
        moved_position = (current_position[0] + direction[0], current_position[1] + direction[1])

        if (moved_position[0] < 0) or (moved_position[0] >= len(self.tiles.matrix[0])):  # TODO change this to in the tile graph? This would allow for teleportation
            return current_position
        elif (moved_position[1] < 0) or (moved_position[1] >= len(self.tiles.matrix)):
            return current_position

        if self.tiles.matrix[moved_position[1], moved_position[0]]:
            return moved_position
        else:
            return current_position

    def get_pixel_coords(self, coords):
        """Return the pixel coordinates from the matrix indices."""
        pixel_x = ((coords[0] % self.dungeon.columns) + 1 / 2) * self.dungeon.square_size
        pixel_y = ((coords[1] % self.dungeon.rows) + 1 / 2) * self.dungeon.square_size

        return pixel_x, pixel_y

    def display_graphics(self):
        pygame.init()

        player = Player(None, None, None, (1, 1), pygame.image.load("player.png").convert_alpha())

        player_surf = player.texture
        player_rect = player_surf.get_rect()
        player_rect.center = player.coords

        monsters = [
            {(9, 7): {"template": "zombie llama", "attack_damage": 20}},
            {(3, 14): {"template": "snail", "hit_points": 40}},
            {(2, 15): {}}
        ]  # TODO fix differences between coordinate systems

        monster_objects = [Monster(list(monster.keys())[0], **list(monster.values())[0]) for monster in monsters]

        for monster in monster_objects:
            print(monster.speed)
            pygame.time.set_timer(monster.move_event, monster.movement)

        clock = pygame.time.Clock()

        while True:
            clock.tick(1000)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_w, pygame.K_UP]:
                        player.coords = Graphics.move_object(self, player.coords, [0, -1])
                    elif event.key in [pygame.K_s, pygame.K_DOWN]:
                        player.coords = Graphics.move_object(self, player.coords, [0, 1])
                    elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                        player.coords = Graphics.move_object(self, player.coords, [1, 0])
                    elif event.key in [pygame.K_a, pygame.K_LEFT]:
                        player.coords = Graphics.move_object(self, player.coords, [-1, 0])
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

                for monster in monster_objects:
                    if event.type == monster.move_event:
                        try:
                            monster_target_square = monster.get_movement_path(player.coords[::-1], level.level_graph)[1]
                        except IndexError:  # TODO this is dependent in movement not collision
                            monster_target_square = player.coords[::-1]
                            exit()

                        monster.coords = monster_target_square


            r_l = (player.coords[0] // self.dungeon.columns) * self.dungeon.columns  # TODO put this in a function
            r_u = r_l + self.dungeon.columns + 1
            c_l = (player.coords[1] // self.dungeon.rows) * self.dungeon.rows
            c_u = c_l + self.dungeon.rows + 1

            self.dungeon.surf.fill((160, 160, 160))

            self.tiles.display(self.dungeon.surf, [r_l, r_u], [c_l, c_u])

            self.walls_top.display(self.dungeon.surf, [r_l, r_u], [c_l, c_u])
            self.walls_bottom.display(self.dungeon.surf, [r_l, r_u], [c_l, c_u])
            self.walls_right.display(self.dungeon.surf, [r_l, r_u], [c_l, c_u])
            self.walls_left.display(self.dungeon.surf, [r_l, r_u], [c_l, c_u])

            player_rect.center = Graphics.get_pixel_coords(self, (player.coords[0], player.coords[1]))
            self.dungeon.surf.blit(player_surf, player_rect)

            for monster in monster_objects:
                monster.rect.center = Graphics.get_pixel_coords(self, monster.coords[::-1])
                if c_l <= monster.coords[0] < c_u-1:  # TODO put this in the monster class maybe or generalise the displaying function
                    if r_l <= monster.coords[1] < r_u-1:  # TODO why have I done it like this???
                        self.dungeon.surf.blit(monster.surf, monster.rect)

            pygame.display.update()


if __name__ == '__main__':
    dungeon = Graphics(level.level_matrix, (0, 0))

    #dungeon = Graphics(hi.dungeon_matrix, np.nonzero(hi.dungeon_matrix)[0][::-1])  # TODO player placement fails

    dungeon.display_graphics()

    tile_graph = level.level_graph
