from GameData import GameData
from TemplatedObject import TemplatedObject

class Item(TemplatedObject):  # Have subclasses for weapons ect
    path = 'items.csv'
    default_items = GameData.csv_to_dict_keys_unique_column(path, 0)
    item_default_attributes = list(default_items['template'].keys())

    def __init__(self, template='template', **kwargs):
        TemplatedObject.__init__(self, template, Item.default_items, kwargs)

    def __str__(self) -> str:  # TODO Implement a nicer thing like tile, do the same for monster too
        return f'Name: {self.name}\nAttack Damage: {self.attack_damage}'


print(Item(attack_damage=1000, name='blunt stone'))
print(Item(template='sword', attack_damage=2))

#print(hi)

# Item()
