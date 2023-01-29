class Level(Game):  # Contains level data object - a dictionary of tile objects - maybe should inherit from game?
    '''Contains methods for the creation of a level'''
    def __init__(self, level_source):
        self.level_data = Level.get_level_data('tiles.csv')

        print(self.level_data)

    @staticmethod
    def get_level_data(source):
        tile_list = Level.get_csv_data_to_dict(source)

        level_data = {}

        print(Game.item_data)

        for tile in tile_list:
            for (k, v) in tile.items():
                if k == 'items':
                    level_data[k] = [Item(Game.item_data[i.strip()]) for i in v.split(',')]

                if k == 'monsters':
                    level_data[k] = [Item(Game.monster_data[i.strip()]) for i in v.split(',')]

            #level_data[tile['coord']] = {k: v.split(',') for (k, v) in tile.items() if k != 'coord'}  # TODO Perhaps strip()

        return level_data