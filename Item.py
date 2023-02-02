from GameData import GameData
from TemplatedObject import TemplatedObject

class Item(TemplatedObject):  # Have subclasses for weapons ect
    path = 'items.csv'
    default_items = GameData.csv_to_dict_keys_unique_column(path, 0)
    #  TODO decide whether the default attributes should be put in this class as they might be needed for __str__

    def __init__(self, template='template', **kwargs):
        TemplatedObject.__init__(self, template, Item.default_items, kwargs)

    # def __str__(self) -> str:  # TODO Implement a nicer thing like tile, do the same for monster too
    #     return f'Name: {self.name.capitalize()}\nAttack Damage: {self.attack_damage}'




#print(Item(template='sword', attack_damage=1010))  # TODO attributes must have _