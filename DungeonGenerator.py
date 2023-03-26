import numpy as np
from random import random, randint
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
    def x_len(self) -> int:
        return abs(self.bounds[1][0] - self.bounds[0][0])

    @property
    def y_len(self) -> int:
        return abs(self.bounds[1][1] - self.bounds[0][1])

    @property
    def t_l(self) -> list:
        return [self.bounds[0][0], self.bounds[1][1]]

    @property
    def t_r(self) -> list:
        return self.bounds[1]

    @property
    def b_l(self) -> list:
        return self.bounds[0]

    @property
    def b_r(self) -> list:
        return [self.bounds[1][0], self.bounds[0][1]]

    @property
    def area(self) -> int:
        return self.x_len * self.y_len

    @property
    def is_indivisible(self) -> bool:
        if (self.x_len < 5) or (self.y_len < 5):
            return True
        else:
            return False

    def check_partition_dimensions(self) -> bool:
        if self.x_len >= 10 and self.y_len >= 10:
            return True

        return False

    def get_split_axis(self) -> int:
        split_axis_pdf = lambda x: 1 / 2 * (math.tanh(x) + 1)
        split_axis = SampleContinuousDistribution.bernoulli_sample(split_axis_pdf,
                                                                   math.log(self.x_len / self.y_len))
        return split_axis


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

        length = randint(2, zone.x_len)
        height = randint(2, zone.y_len)

        print("-----")
        print(zone.b_l, zone.b_r, zone.t_l, zone.t_r)

        print("xlen", zone.x_len, "ylen", zone.y_len)

        print(zone.b_l[0], zone.b_r[0] - length)
        print(zone.b_l[1], zone.t_l[1] - height)
        print(length, height, zone.x_len, zone.y_len)

        b_l_x = randint(zone.b_l[0], zone.b_r[0] - length)
        b_l_y = randint(zone.b_l[1], zone.t_l[1] - height)

        # b_l_x = zone.bounds[0][0]
        # b_l_y = zone.bounds[0][1]

        room = [(b_l_x, b_l_y), (b_l_x+length-1, b_l_y+height-1)] # TODO put back?
        #room = [(b_l_x, b_l_y), (b_l_x + zone.x_len, b_l_y + zone.y_len)]

        return room


    def partition_partition(self, partition: PartitionNode) -> None:
        if PartitionNode.check_partition_dimensions(partition):
            if Dungeon.random_split_area(partition.area):
                split_axis = PartitionNode.get_split_axis(partition)
                Dungeon.split_partition(self, (split_axis + 1) % 2, partition)

                return

        self.dungeon_tree.active_end_nodes.remove(partition.index)

    @staticmethod
    def random_split_area(area: float, min_a: int=4, max_a: int=400) -> int:  # TODO if outside of the bounds, return no split, might need to change the other bit that decides on the split
        pdf = lambda x: (x-min_a)/(max_a-min_a)

        return SampleContinuousDistribution.bernoulli_sample(pdf, area)

    @staticmethod
    def get_partition_split_point(u_b, l_b):
        d = u_b - l_b
        split_point_cdf = lambda x: (d*math.sin(4*math.pi*x/d) - 8*d*math.sin(2*math.pi*x/d) + 12*math.pi*x) / \
                                    (12*math.pi*d)
        split_point = round(SampleContinuousDistribution.single_sample(split_point_cdf, (u_b + l_b) / 2) + l_b)

        return split_point

    @staticmethod
    def set_new_partition_bounds(initial_bounds: list[list[int]], split_point: int, direction: int) -> list:
        partition_bounds = []

        for new_partition in range(2):
            sub_partition_bounds = [[None, None], [None, None]]
            sub_partition_bounds[new_partition] = initial_bounds[new_partition]

            new_bound_index = (new_partition + 1) % 2
            sub_partition_bounds[new_bound_index][direction] = split_point
            sub_partition_bounds[new_bound_index][(direction + 1) % 2] = \
                initial_bounds[new_bound_index][(direction + 1) % 2]

            partition_bounds.append(sub_partition_bounds)

        return partition_bounds


    def split_partition(self, direction: int, partition: PartitionNode) -> None:
        initial_bounds = partition.bounds
        l_b = initial_bounds[0][direction] + 2
        u_b = initial_bounds[1][direction] - 2

        d = u_b - l_b
        if d == 0:
            raise ValueError("Upper bound an Lower Bound for the split range cannot be equal!")

        split_point = Dungeon.get_partition_split_point(u_b, l_b)

        sub_par_1_b, sub_par_2_b = Dungeon.set_new_partition_bounds(initial_bounds, split_point, direction)

        self.dungeon_tree.add_node(PartitionNode(sub_par_1_b, partition.index))
        self.dungeon_tree.add_node(PartitionNode(sub_par_2_b, partition.index))


class DungeonAnalysis:
    def __init__(self, sim_count: int) -> None:
        self.count = sim_count
        self.dungeon_simulations = [Dungeon([[0, 0], [100, 100]]) for i in range(self.count)]

    def graph_zone_distribution(self):
        raise NotImplementedError

    def generate_dungeon_data(self):
        self.mean_zone_area = sum([dungeon.area for dungeon in self.dungeon_simulations])/self.count
        raise NotImplementedError



hi = Dungeon([[0, 0], [50, 50]])
hi.display_colour_map()
