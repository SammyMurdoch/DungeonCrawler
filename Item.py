class Item:  # Have subclasses for weapons ect
    def __init__(self, item_data: dict):
        self.name = item_data['name']
        self.attack_damage = item_data['attack_damage']

    def __str__(self) -> str:
        return f'Attack Damage: {self.attack_damage}'

