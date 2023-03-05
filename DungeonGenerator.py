import numpy as np
from random import randint, random
import matplotlib.pyplot as plt
import math

np.set_printoptions(threshold=np.inf)
class PartitionTree:
    def __init__(self, root):
        root_id = 0
        self.nodes = {root_id: PartitionNode(root, None)}
        self.end_nodes = {root_id}
        self.active_end_nodes = {root_id}


    def add_node(self, value, parent):
        node_index = len(self.nodes)
        self.nodes[node_index] = PartitionNode(value, parent)

        if parent is not None:
            self.nodes[parent].add_child(node_index)
            if parent in self.end_nodes:
                self.end_nodes.remove(parent)
                self.active_end_nodes.remove(parent)

        if not self.nodes[node_index].is_indivisible:
            self.active_end_nodes.add(node_index)

        self.end_nodes.add(node_index)

    def __len__(self):
        return len(self.nodes)

    @property
    def is_complete(self):
        if not len(self.active_end_nodes):
            return True

        return False


class PartitionNode:
    def __init__(self, bounds, parent):
        self.bounds = bounds
        self.parent = parent
        self.children = []
        self.room = None

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return f'Bounds: {self.bounds}\nParent: {self.parent}\nChildren: {self.children}\n'

    @property
    def x_len(self):
        return self.bounds[1][0] - self.bounds[0][0]

    @property
    def y_len(self):
        return self.bounds[1][1] - self.bounds[0][1]

    @property
    def is_indivisible(self):
        if self.x_len < 5 or self.y_len < 5:
            return True
        else:
            return False

class Dungeon:
    def __init__(self, bounds):
        self.dungeon_tree = PartitionTree(bounds)

        while not self.dungeon_tree.is_complete:
            for partition in self.dungeon_tree.active_end_nodes.copy():
                Dungeon.partition_partition(self, partition)

        for zone in self.dungeon_tree.end_nodes:
            zone_object = self.dungeon_tree.nodes[zone]

            length = randint(2, self.dungeon_tree.nodes[zone].x_len)
            height = randint(2, self.dungeon_tree.nodes[zone].y_len)

            b_l_x = randint(zone_object.bounds[0][0], zone_object.bounds[1][0] - length)
            b_l_y = randint(zone_object.bounds[0][1], zone_object.bounds[1][1] - height)

            zone_object.room = [(b_l_x, b_l_y), (b_l_x+length, b_l_y+height)]

        self.dungeon_matrix = np.zeros((bounds[1][0], bounds[1][1]))

        for zone in self.dungeon_tree.end_nodes:
            zone_object = self.dungeon_tree.nodes[zone]  # TODO this should just be an attribute
            r = zone_object.room

            self.dungeon_matrix[r[0][0]: r[1][0], r[0][1] + 1: r[1][1] + 1] = 1

        print(self.dungeon_matrix)


    def partition_partition(self, partition):
        x_len = self.dungeon_tree.nodes[partition].x_len
        y_len = self.dungeon_tree.nodes[partition].y_len
        # if self.dungeon_tree.nodes[partition].x_len < 5: maybe put this back and make splitting based on a probability distribution
        #     Dungeon.split(self, 1, partition)
        # elif self.dungeon_tree.nodes[partition].y_len < 5:
        #     Dungeon.split(self, 0, partition)
        # else:
        #     Dungeon.split(self, randint(0, 1), partition)

        if x_len >= 5 and y_len >=5:
            if Dungeon.random_split((x_len, y_len)):
                Dungeon.split(self, randint(0, 1), partition)

    @staticmethod
    def random_split(dim, min_a=4, max_a=100):  # TODO if outside of the bounds, return no split, might need to change the other bit that decides on the split
        p_f = lambda x: (x-min_a)/(max_a-min_a)
        probability = p_f(math.prod(dim))

        if random() <= probability:
            return True

        return False

    def split(self, direction, partition):
        initial_bounds = self.dungeon_tree.nodes[partition].bounds
        l_b = initial_bounds[0][direction] + 2
        u_b = initial_bounds[1][direction] - 2

        split_point = randint(l_b, u_b)

        sub_par_1_b = [initial_bounds[0], [None, None]]
        sub_par_2_b = [[None, None], initial_bounds[1]]

        sub_par_1_b[1][direction] = split_point  # TODO function this
        sub_par_1_b[1][(direction+1) % 2] = initial_bounds[1][(direction+1) % 2]

        sub_par_2_b[0][direction] = split_point
        sub_par_2_b[0][(direction+1) % 2] = initial_bounds[0][(direction+1) % 2]

        self.dungeon_tree.add_node(sub_par_1_b, partition)
        self.dungeon_tree.add_node(sub_par_2_b, partition)

hi = Dungeon(([0, 0], [10, 16]))