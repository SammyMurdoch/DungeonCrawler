from GameData import GameData

class TemplatedObject:
    
    def __init__(self, template, templates, attribute_dict):
        self.default_attributes = list(templates['template'].keys())  # TODO Should default attributes be a class variable instead

        if template not in templates:
            raise ValueError('Invalid Template')

        template_dict = templates[template]

        for attr in self.default_attributes:
            if attr not in list(template_dict.keys()) + list(attribute_dict.keys()):  # TODO this currently doesn't run as it will replace things in template
                raise ValueError(f'Missing attribute: {attr}')

            if attr in attribute_dict:
                setattr(TemplatedObject, attr, attribute_dict[attr])
            else:
                setattr(TemplatedObject, attr, template_dict[attr])

    def __str__(self) -> str:  # TODO this is from tile, incorporate tile into this
        displayed_string = ""

        for attr in self.default_attributes:
            displayed_string += f'{attr.capitalize().replace("_", " ")}: '  # TODO make a function to format attributes

            tile_attribute = getattr(self, attr)

            if tile_attribute is None:
                displayed_string += f'None\n'

            else:
                if isinstance(tile_attribute, int) or isinstance(tile_attribute, str):
                    displayed_string += str(getattr(self, attr)) + '\n'
                elif hasattr(tile_attribute, '__iter__'):
                    displayed_string += f'{", ".join([hi.name for hi in tile_attribute])}\n'
                else:
                    displayed_string += str(getattr(self, attr)) + '\n'  # TODO is there a better way, same line 2x



        return displayed_string
