from GameData import GameData

class Item:  # Have subclasses for weapons ect
    path = 'items.csv'
    default_items = GameData.csv_to_dict_keys_unique_column(path, 0)
    item_default_attributes = list(default_items['template'].keys())

    def __init__(self, template='template', **kwargs):
        if template not in Item.default_items:
            raise ValueError('Invalid Template')
        template = Item.default_items[template]

        for attr in Item.item_default_attributes:
            if attr not in list(template.keys()) + list(kwargs.keys()):
                raise ValueError(f'Missing attribute: {attr}')
            if attr in kwargs:
                setattr(Item, attr, kwargs[attr])

            else:
                setattr(Item, attr, template[attr])

    def __str__(self) -> str:  # TODO Implement a nicer thing like tile, do the same for monster too
        return f'Name: {self.name}\nAttack Damage: {self.attack_damage}'


print(Item(attack_damage=1000, name='blunt stone'))
print(Item(template='sword'))

#print(hi)

Item()
