from Monster import Monster
from Item import Item

class Tile:
    def __init__(self, tile_data):
        self.items = tile_data['items']
        self.monsters = tile_data['monsters']

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