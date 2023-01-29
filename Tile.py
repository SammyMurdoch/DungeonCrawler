from Monster import Monster
from Item import Item

class Tile:
    def __init__(self, tile_data):
        if tile_data['items'] is None:
            self.items = None

        else:
            self.items = [Item(item) for item in tile_data['items']]

        if tile_data['monsters'] is None:
            self.monsters = None

        else:
            self.monsters = [Monster(monster) for monster in tile_data['monsters']]

    # def __str__(self) -> str:
    #     return f'Items: {self.items}, Monsters: {self.monsters}'
    #
    # def __add__(self, other):
    #     if isinstance(other) == Item:
    #         self.items[other] = []  # get data from items class
    #         pass
    #
    #     if isinstance(other) == Monster:
    #         #self.monsters
    #         pass