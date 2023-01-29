class Tile:
    def __init__(self, coord: tuple, level):
        self.items = tile_data['items']
        self.monsters = tile_data['monsters']

        pass

    def __str__(self) -> str:
        return f'{self.coord}:\nItems: {self.items}, Monsters: {self.monsters}'

    def __add__(self, other) -> 'Tile':
        if isinstance(other) == Item:
            #self.items[other] = []  # get data from items class
            pass

        if isinstance(other) == Monsters:
            #self.monsters
            pass