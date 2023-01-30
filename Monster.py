from GameData import GameData
from TemplatedObject import TemplatedObject

class Monster(TemplatedObject):
    path = 'monsters.csv'
    default_items = GameData.csv_to_dict_keys_unique_column(path, 0)

    def __init__(self, template='template', **kwargs):
        TemplatedObject.__init__(self, template, Monster.default_items, kwargs)

    def __str__(self) -> str:
        return f'{self.name}:\nHit Points: {self.hit_points}, Attack Damage: {self.attack_damage}'

    def attack(self):
        return self.attack_damage


print(Monster(attack_damage=5, name='zombie rabbit', template='snail'))