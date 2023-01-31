from Monster import Monster
from Item import Item

class Tile:  # TODO I probably also want this as as a templated class
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

    def __add__(self, other):
        if isinstance(other) == Item:
            if self.items is None:
                self.items = [other]

            else:
                self.items.append(other)

        if isinstance(other) == Monster:
            if self.monsters is None:
                self.monsters = [other]

            else:
                self.monsters.append(other)
