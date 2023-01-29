from GameData import GameData

class Item:  # Have subclasses for weapons ect
    default_items = GameData.csv_to_dict_keys_unique_column("items.csv", 0)

    def __init__(self, item_type):
        self.name = item_type
        self.attack_damage = self.default_items[self.name]['attack_damage']

    def __str__(self) -> str:
        return f'{self.name}:\nAttack Damage: {self.attack_damage}'

