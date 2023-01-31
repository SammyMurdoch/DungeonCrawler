from GameData import GameData
from TemplatedObject import TemplatedObject

class Monster(TemplatedObject):
    path = 'monsters.csv'
    default_items = GameData.csv_to_dict_keys_unique_column(path, 0)

    def __init__(self, template='template', **kwargs):
        TemplatedObject.__init__(self, template, Monster.default_items, kwargs)

    def attack(self):
        return self.attack_damage


print(Monster(template='snail', attack_damage='1'))