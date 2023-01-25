import pandas as pd

class Tile:
    def __init__(self, tile_data: dict):
        self.coord = tile_data["coord"]
        self.items = tile_data["items"]
        self.monsters = tile_data["monsters"]

    def __str__(self) -> str:
        return f"{self.coord}:\nItems: {self.items}, Monsters: {self.monsters}"


class Item:  # Have subclasses for weapons ect
    def __init__(self, item_data):
        self.name = item_data["name"]
        self.attack_damage = item_data["attack_damage"]

    def __str__(self):
        return f"Attack Damage: {self.attack_damage}"


class Monster:
    def __init__(self, monster_data: dict):
        self.name = monster_data["name"]
        self.hit_points = monster_data["hit_points"]
        self.attack_damage = monster_data["attack_damage"]

    def __str__(self):
        return f"Hit Points: {self.hit_points}, Attack Damage: {self.attack_damage}"


tile = Tile({"coord": (0, 0),
    "items": [Item({"name": "Sword", "attack_damage": 2}), Item({"name": "Shield", "attack_damage": 0})],
    "monsters": [Monster({"name": "Zombie", "hit_points": 10, "attack_damage": 2})]})


print(tile)


tiles_df = pd.read_csv('tiles.csv', encoding='utf-8-sig')
tiles = tiles_df.to_dict(orient='records')

items_df = pd.read_csv('monsters.csv', encoding='utf-8-sig')
items = items_df.to_dict(orient='records')

monsters_df = pd.read_csv('monsters.csv', encoding='utf-8-sig')
monsters = monsters_df.to_dict(orient='records')

print(tiles)
print(items)
print(monsters)