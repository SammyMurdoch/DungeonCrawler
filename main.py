import pandas as pd

# class Item:  # Have subclasses for weapons ect
#     def __init__(self, item_data: dict):
#         self.name = item_data["name"]
#         self.attack_damage = item_data["attack_damage"]
#
#     def __str__(self) -> str:
#         return f"Attack Damage: {self.attack_damage}"
#
#
# class Monster:
#     def __init__(self, monster_data: dict):
#         self.name = monster_data["name"]
#         self.hit_points = monster_data["hit_points"]
#         self.attack_damage = monster_data["attack_damage"]
#
#     def __str__(self) -> str:
#         return f"Hit Points: {self.hit_points}, Attack Damage: {self.attack_damage}"

# class Game:  # Class for running the game
#     @staticmethod
#     def get_csv_data_to_dict(source):
#         df = pd.read_csv(source, encoding='utf-8-sig', header=0)
#         df_rows = df.to_dict(orient='records')
#
#
#
#
#     item_data = get_csv_data_to_dict('items.csv')
#     monster_data = get_csv_data_to_dict('monsters.csv')


# class Level(Game):  # Contains level data object - a dictionary of tile objects - maybe should inherit from game?
#     """Contains methods for the creation of a level"""
#     def __init__(self, level_source):
#         self.level_data = Level.get_level_data('tiles.csv')
#
#         print(self.level_data)
#
#     @staticmethod
#     def get_level_data(source):
#         tile_list = Level.get_csv_data_to_dict(source)
#
#         level_data = {}
#
#         print(Game.item_data)
#
#         for tile in tile_list:
#             for (k, v) in tile.items():
#                 if k == 'items':
#                     level_data[k] = [Item(Game.item_data[i.strip()]) for i in v.split(',')]
#
#                 if k == 'monsters':
#                     level_data[k] = [Item(Game.monster_data[i.strip()]) for i in v.split(',')]
#
#             #level_data[tile['coord']] = {k: v.split(',') for (k, v) in tile.items() if k != 'coord'}  # TODO Perhaps strip()
#
#         return level_data



hi_df = pd.read_csv('tiles.csv')

key_name = hi_df.columns[0]

hi_df_dict = hi_df.to_dict(orient='records')

hi_dict = {}

for h in hi_df_dict:
    key = h[key_name]

    value = {k: exec(v) for (k, v) in h.items() if k != key_name}

    hi_dict[key] = value

print(hi_dict)


# class Tile:
#     def __init__(self, coord: tuple, level):
#         self.items = tile_data["items"]
#         self.monsters = tile_data["monsters"]
#
#         pass
#
#     def __str__(self) -> str:
#         return f"{self.coord}:\nItems: {self.items}, Monsters: {self.monsters}"
#
#     def __add__(self, other) -> 'Tile':
#         if isinstance(other) == Item:
#             #self.items[other] = []  # get data from items class
#             pass
#
#         if isinstance(other) == Monsters:
#             #self.monsters
#             pass

#
# tile = Tile({"coord": (0, 0),
#     "items": [Item({"name": "Sword", "attack_damage": 2}), Item({"name": "Shield", "attack_damage": 0})],
#     "monsters": [Monster({"name": "Zombie", "hit_points": 10, "attack_damage": 2})]})
#
#
#
# print(tile)
