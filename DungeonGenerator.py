import numpy as np
from random import random
import matplotlib.pyplot as plt
from matplotlib import colors
import math
from scipy.optimize import fsolve

np.set_printoptions(threshold=np.inf)


class SampleContinuousDistribution:
    @staticmethod
    def generate_sample(cdf: callable, n: int, x0: float) -> list:
        samples = []

        for i in range(n):
            r = random()
            samples.append((fsolve(lambda x: cdf(x) - r, np.array([x0]))[0]))

        return samples

    @staticmethod
    def single_sample(cdf: callable, x0: float) -> float:
        return SampleContinuousDistribution.generate_sample(cdf, 1, x0)[0]

    @staticmethod
    def bernoulli_sample(pdf: callable, x: float) -> int:
        r = random()

        if r < pdf(x):
            return 1

        return 0


class TreeNode:
    def __init__(self, parent: int=None, children: set[int]=None) -> None:
        self.index = None
        self.parent_index = parent
        self.children_indices = children

    def __str__(self) -> str:
        return f'Parent: {self.parent_index}, Children: {self.children_indices}'

    def add_child(self, child: int) -> None:
        if self.children_indices is None:
            self.children_indices = {child}
        else:
            self.children_indices.add(child)


class Tree:
    def __init__(self, root: TreeNode=None) -> None:
        self.nodes = {}
        self.root = None

        if root is not None:
            self.add_node(root)

    def add_node(self, tree_node: TreeNode) -> None:
        tree_node.index = len(self)

        if tree_node.parent_index is None:
            if self.root is None:
                self.nodes[tree_node.index] = tree_node
                self.root = tree_node.index

            else:
                raise ValueError("Node must have a parent to add it to the tree.")
        else:
            if tree_node.parent_index in self.nodes:
                self.nodes[tree_node.index] = tree_node
                self.nodes[tree_node.parent_index].add_child(tree_node.index)
            else:
                raise ValueError("Parent not in the tree.")

    def __len__(self) -> int:
        try:
            return len(self.nodes)
        except (AttributeError, TypeError):
            return 0

class PartitionTree(Tree):
    def __init__(self, root=None) -> None:
        if root is not None:
            self.end_nodes = {len(self)}
            self.active_end_nodes = {len(self)}
        else:
            self.end_nodes = None
            self.active_end_nodes = None

        super().__init__(root)

    def __str__(self) -> str:
        s = ""

        for node in self.nodes:
            s += f'Index: {node}, {str(self.nodes[node])}\n'

        s += f'\nEnd Nodes: {self.end_nodes}\nActive End Nodes: {self.active_end_nodes}'

        return s

    def add_node(self, node: TreeNode) -> None:
        super().add_node(node)

        if self.end_nodes is None:
            self.end_nodes = {node.index}
            self.active_end_nodes = {node.index}
        else:
            self.end_nodes.add(node.index)
            self.active_end_nodes.add(node.index)

            if node.parent_index in self.end_nodes:
                self.end_nodes.remove(node.parent_index)
                self.active_end_nodes.remove(node.parent_index)

    @property
    def is_complete(self) -> bool:
        if self.active_end_nodes is None:
            return False

        if not self.active_end_nodes:
            return True

        return False


class PartitionNode(TreeNode):
    def __init__(self, bounds: list[list[int]], parent: int=None, room: list[list[int]]=None) -> None:
        super().__init__(parent)

        self.bounds = bounds
        self.room = room

    def __str__(self) -> str: # TODO change to print out all attributes in a certain list
        return f'Bounds: {self.bounds}, Room: {self.room}, {super().__str__()}'

    @property
    def x_len(self) -> float:
        return abs(self.bounds[1][0] - self.bounds[0][0])

    @property
    def y_len(self) -> float:
        return abs(self.bounds[1][1] - self.bounds[0][1])

    @property
    def area(self) -> float:
        return self.x_len * self.y_len

    @property
    def is_indivisible(self) -> bool:
        if (self.x_len < 5) or (self.y_len < 5):
            return True
        else:
            return False
''
#class EndPartitionNode(PartitionNode):




class Dungeon:
    def __init__(self, bounds: list[list[int]]) -> None:
        self.bounds = bounds
        self.dungeon_tree = Dungeon.generate_dungeon_tree(self)
        self.zone_objects = [self.dungeon_tree.nodes[zone] for zone in self.dungeon_tree.end_nodes]

        for zone in self.zone_objects:
            zone.room = Dungeon.generate_room(zone)

        self.dungeon_matrix = Dungeon.generate_dungeon_matrix(self)

    def generate_dungeon_tree(self):
        self.dungeon_tree = PartitionTree(PartitionNode(self.bounds))

        while not self.dungeon_tree.is_complete:
            for partition in self.dungeon_tree.active_end_nodes.copy():
                Dungeon.partition_partition(self, self.dungeon_tree.nodes[partition])

        return self.dungeon_tree

    def generate_dungeon_matrix(self) -> np.ndarray:
        dungeon_matrix = np.zeros((self.bounds[1][1], self.bounds[1][0]))

        for i, zone in enumerate(self.zone_objects):
            r = zone.room

            dungeon_matrix[r[0][1]: r[1][1], r[0][0]: r[1][0]] = i+1  # Flipped due to matrix geometry

        return dungeon_matrix

    def display_colour_map(self) -> None:
        colour_values = np.linspace(0, 270, len(self.dungeon_tree.end_nodes) + 2)

        new_colour_values = np.empty((len(colour_values), 3))

        for i, colour in enumerate(colour_values):
            new_colour_values[i] = [colour / 360, 0.5, 0.5]

        for i, row in enumerate(new_colour_values):
            new_colour_values[i] = colors.hsv_to_rgb(tuple(row))

        c_map = colors.ListedColormap(new_colour_values)

        plt.imshow(self.dungeon_matrix, cmap=c_map)
        plt.show()

    @staticmethod
    def generate_room(zone: PartitionNode) -> list:
        print(f'Zone: {zone.bounds}')

        # length = randint(2, self.dungeon_tree.nodes[zone].x_len)
        # height = randint(2, self.dungeon_tree.nodes[zone].y_len)

        # b_l_x = randint(zone_object.bounds[0][0], zone_object.bounds[1][0] - length)
        # b_l_y = randint(zone_object.bounds[0][1], zone_object.bounds[1][1] - height)

        b_l_x = zone.bounds[0][0]
        b_l_y = zone.bounds[0][1]

        # zone_object.room = [(b_l_x, b_l_y), (b_l_x+length-1, b_l_y+height-1)] # TODO put back?
        room = [(b_l_x, b_l_y), (b_l_x + zone.x_len, b_l_y + zone.y_len)]

        return room


    def partition_partition(self, partition: PartitionNode) -> None:
        # if self.dungeon_tree.nodes[partition].x_len < 5: maybe put this back and make splitting based on a probability distribution
        #     Dungeon.split(self, 1, partition)
        # elif self.dungeon_tree.nodes[partition].y_len < 5:
        #     Dungeon.split(self, 0, partition)
        # else:
        #     Dungeon.split(self, randint(0, 1), partition)

        if partition.x_len >= 10 or partition.y_len >= 10: # TODO and or or?
            if Dungeon.random_split([partition.x_len, partition.y_len]):
                #split_axis_pdf = lambda x: (1/math.pi) * (math.atan(x) + math.pi/2)
                split_axis_pdf = lambda x: 1/2 * (math.tanh(x) + 1)

                split_axis = SampleContinuousDistribution.bernoulli_sample(split_axis_pdf,
                                                                           math.log(partition.x_len/partition.y_len))

                if Dungeon.split_partition(self, (split_axis + 1) % 2, partition):
                    return

        self.dungeon_tree.active_end_nodes.remove(partition.index)

    @staticmethod
    def random_split(dim: list, min_a: int=4, max_a: int=400) -> int:  # TODO if outside of the bounds, return no split, might need to change the other bit that decides on the split
        pdf = lambda x: (x-min_a)/(max_a-min_a)

        return SampleContinuousDistribution.bernoulli_sample(pdf, math.prod(dim))

    def split_partition(self, direction: int, partition: PartitionNode) -> bool:
        initial_bounds = partition.bounds
        l_b = initial_bounds[0][direction] + 2
        u_b = initial_bounds[1][direction] - 2

        d = u_b - l_b
        if d == 0:
            return False

        split_point_cdf = lambda x: (d*math.sin(4*math.pi*x/d) - 8*d*math.sin(2*math.pi*x/d) + 12*math.pi*x) / \
                                    (12*math.pi*d)
        split_point = round(SampleContinuousDistribution.single_sample(split_point_cdf, (u_b + l_b) / 2) + l_b)

        sub_par_1_b = [initial_bounds[0], [None, None]]
        sub_par_2_b = [[None, None], initial_bounds[1]]

        sub_par_1_b[1][direction] = split_point  # TODO function this
        sub_par_1_b[1][(direction+1) % 2] = initial_bounds[1][(direction+1) % 2]

        sub_par_2_b[0][direction] = split_point
        sub_par_2_b[0][(direction+1) % 2] = initial_bounds[0][(direction+1) % 2]

        self.dungeon_tree.add_node(PartitionNode(sub_par_1_b, partition.index))
        self.dungeon_tree.add_node(PartitionNode(sub_par_2_b, partition.index))

        return True


class DungeonAnalysis:
    def __init__(self, sim_count) -> None:
        self.count = sim_count
        self.dungeon_simulations = [Dungeon([[0, 0], [100, 100]]) for i in range(self.count)]

    def graph_zone_distribution(self):
        raise NotImplementedError

    def generate_dungeon_data(self):
        self.mean_zone_area = sum([dungeon.area for dungeon in self.dungeon_simulations])/self.count
        raise NotImplementedError



hi = Dungeon([[0, 0], [100, 100]])
hi.display_colour_map()
#print(hi.dungeon_matrix)

print("hi")

