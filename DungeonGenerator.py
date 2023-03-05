import numpy as np
from random import randint

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
        if self.x_len < 5 and self.y_len < 5:
            return True
        else:
            return False

class Dungeon:
    def __init__(self, bounds):
        self.dungeon_tree = PartitionTree(bounds)

        while not self.dungeon_tree.is_complete:
            for partition in self.dungeon_tree.active_end_nodes:
                Dungeon.partition_partition(self, partition)

            for leaf in self.dungeon.tree:
                print(leaf)

    def partition_partition(self, partition):
        if self.dungeon_tree.nodes[partition].x_len < 5:
            Dungeon.split(self, 1, partition)
        elif self.dungeon_tree.nodes[partition].y_len < 5:
            Dungeon.split(self, 0, partition)
        else:
            Dungeon.split(self, randint(0, 1), partition)

    def split(self, direction, partition):
        initial_bounds = self.dungeon_tree.nodes[partition].bounds
        l_b = initial_bounds[0][direction] + 2
        u_b = initial_bounds[1][direction] - 2

        print(l_b, u_b)

        split_point = randint(l_b, u_b)

        sub_par_1_b = [initial_bounds[0], [None, None]]
        sub_par_2_b = [[None, None], initial_bounds[1]]

        sub_par_1_b[1][direction] = split_point
        sub_par_1_b[1][(direction+1) % 2] = initial_bounds[1][(direction+1) % 2]

        sub_par_2_b[0][direction] = split_point
        sub_par_2_b[0][(direction+1) % 2] = initial_bounds[0][(direction+1) % 2]

        self.dungeon_tree.add_node(sub_par_1_b, partition)
        self.dungeon_tree.add_node(sub_par_2_b, partition)

hi = Dungeon(([0, 0], [9, 9]))