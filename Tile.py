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

    def __str__(self) -> str:
        displayed_attributes = ['items', 'monsters']
        displayed_string = ""

        for attr in displayed_attributes:
            displayed_string += f'{attr.capitalize()}: '

            tile_attribute = getattr(self, attr)

            if tile_attribute is None:
                displayed_string += f'None\n'

            else:
                if isinstance(tile_attribute, list):
                    displayed_string += f'{", ".join([hi.name for hi in tile_attribute])}\n'

                if isinstance(tile_attribute, str):
                    displayed_string += str(getattr(self, attr))

        return displayed_string


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