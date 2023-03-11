from GameData import GameData
from TemplatedObject import TemplatedObject
import networkx as nx
import random
import pygame

class Monster(TemplatedObject):
    path = 'monsters.csv'
    default_items = GameData.csv_to_dict_keys_unique_column(path, 0)

    def __init__(self, location, template='template', **kwargs):
        super().__init__(self, template, Monster.default_items, kwargs)
        self.coords = location

        self.surf = pygame.image.load(self.texture).convert_alpha()  # TODO put all graphic things in a different place

        self.rect = self.surf.get_rect()
        self.rect.center = self.coords

        self.movement = self.speed
        self.move_event = pygame.USEREVENT


    def attack(self):
        return self.attack_damage


    def get_movement_path(self, player_location, level_graph):  # TODO call function when the player moves and and then every second or so while they are moving
        random_shortest_path = random.choice(list(nx.all_shortest_paths(level_graph, self.coords, player_location)))

        return random_shortest_path

    #def move_monster(self):
#print(Monster(template='snail', attack_damage='1'))