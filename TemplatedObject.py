from GameData import GameData

class TemplatedObject:
    def __init__(self, attribute_list, template=None, **kwargs):  #pass in a template which contains a list of required attribute and possibly a dictionary of attributes to edit
        print(kwargs)

        if template is not None:
            for attr in templates[template_source_data].keys():
                print("hi")



        print(templates)


TemplatedObject({'path': 'items.csv', 'column': 0}, name='blunt stone')






