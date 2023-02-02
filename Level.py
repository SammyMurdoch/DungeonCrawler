from GameData import GameData
from Tile import Tile

class Level:
    def __init__(self, level_source):
        self.level_data = GameData.csv_to_dict_keys_unique_column(level_source, 0)

        self.tiles = {tile: Tile(tile_data) for (tile, tile_data) in self.level_data.items()}

level = Level("tiles.csv")

print(level.level_data.keys())

for tile in level.level_data.keys():
    print(level.tiles[tile])


