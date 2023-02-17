from GameData import GameData
from TemplatedObject import TemplatedObject
import networkx as nx

class Monster(TemplatedObject):
    path = 'monsters.csv'
    default_items = GameData.csv_to_dict_keys_unique_column(path, 0)

    def __init__(self, location, removethislater, template='template', **kwargs):
        TemplatedObject.__init__(self, template, Monster.default_items, kwargs)
        self.coords = location
        self.texture = removethislater  # TODO CHANGE THIS TO A COLUMN IN THE CSV

    def attack(self):
        return self.attack_damage

    def get_movement_path(self, player_location, level_graph):  # TODO call function when the player moves and and then every second or so while they are moving
        return nx.shortest_path(level_graph, self.coords, player_location)


#print(Monster(template='snail', attack_damage='1'))