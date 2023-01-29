from GameData import GameData

class Monster:
    default_monsters = GameData.csv_to_dict_keys_unique_column('monsters.csv', 0)

    def __init__(self, monster_type):
        self.name = monster_type
        self.hit_points = self.default_monsters[self.name]['hit_points']
        self.attack_damage = self.default_monsters[self.name]['attack_damage']

    def __str__(self) -> str:
        return f'{self.name}:\nHit Points: {self.hit_points}, Attack Damage: {self.attack_damage}'

    def attack(self):
        return self.attack_damage