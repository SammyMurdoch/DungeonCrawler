class Monster:
    def __init__(self, monster_data: dict):
        self.name = monster_data['name']
        self.hit_points = monster_data['hit_points']
        self.attack_damage = monster_data['attack_damage']

    def __str__(self) -> str:
        return f'Hit Points: {self.hit_points}, Attack Damage: {self.attack_damage}'