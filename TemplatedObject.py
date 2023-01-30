from GameData import GameData

class TemplatedObject:
    def __init__(self, template, templates, attribute_dict):
        default_attributes = list(templates['template'].keys())

        if template not in templates:
            raise ValueError('Invalid Template')

        template_dict = templates[template]

        for attr in default_attributes:
            if attr not in list(template_dict.keys()) + list(attribute_dict.keys()):
                raise ValueError(f'Missing attribute: {attr}')
            if attr in attribute_dict:
                setattr(TemplatedObject, attr, attribute_dict[attr])

            else:
                setattr(TemplatedObject, attr, template_dict[attr])

#TemplatedObject('sword', {'template': {'attack_damage': 4, 'name': 'template'}, 'sword': {'attack_damage': 4, 'name': 'sword'}} , {'name': 'blunt stone'})






